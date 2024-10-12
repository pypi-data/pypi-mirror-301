"""This module contains TabularFileTableBuilder class for building tabular file tables.

The TabularFileTableBuilder class is used to build tabular file tables from
schema-matched tabular files listed in the `files` table. It expects the dataset to be
populated with the primary tables (e.g. `subjects`, `sessions`, `acquisitions`, and
`files`).

As this can be both time and resource-intensive, it is recommended to run this process
in a separate script or as a background task.
"""

import copy
import csv
from pathlib import Path

import duckdb
import flywheel
import pandas as pd

from ..models import DataModel
from .admin_helpers import (
    add_parent_info,
    enforce_field_types,
    get_container_path,
    get_delimiter,
    get_table_schema,
    match_table_schema,
    sanitize_table_name,
    save_schema,
    save_table,
    validate_dataset_table,
)


class TabularFileTableBuilder:
    """Class for building tabular file tables from schema-matched tabular files."""

    def __init__(
        self, dataset_path: Path, files_cache_path: Path, fw_client: flywheel.Client
    ):
        """Constructor for the TabularFileTableBuilder class.

        Args:
            dataset_path (Path): Path to the dataset directory
            files_cache_path (Path): Path to the files cache directory
            fw_client (flywheel.Client): Flywheel sdk client
        """
        self.dataset_path = dataset_path
        self.sdk_client = fw_client

        # Ensure the files cache path exists
        files_cache_path.mkdir(parents=True, exist_ok=True)
        self.files_cache_path = files_cache_path

        # Establish the connection to the DuckDB database
        self.duckdb_conn = duckdb.connect()

        # Reserve a dictionary for matched schema mappings
        self.schema_mappings = {}

    def save_schema_mappings(self) -> None:
        """Save matched schemas and referenced files to the dataset directory.

        Iterates through all referenced files of the schema and saves them as a parquet
        table partition.
        """
        # Loop through and save the mapped schemas to the dataset directory
        # Each referenced file is saved as a partition of the schema table
        for schema_key, mapped_schema in self.schema_mappings.items():
            # Copy the schema to prevent changes to the original schema
            schema_to_save = copy.deepcopy(mapped_schema)
            schema_to_save.pop("files")

            # Sanitize the table name to conform to GA4GH DataConnect requirements
            # TODO: Offer an admin method to change the table name and other attributes
            schema_name = Path(sanitize_table_name(schema_key)).stem
            schema_to_save["id"] = schema_name

            save_schema(self.dataset_path, schema_name, schema_to_save)

            # Iterate through all referenced files of the schema and save them as table
            # partitions in the dataset
            for file in mapped_schema.get("files", []):
                fw_file = self.sdk_client.get_file(file["file_id"])
                file_path = self.files_cache_path / get_container_path(fw_file)
                file_path /= file["name"]

                # Ensure file is downloaded
                if not file_path.exists():
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    self.sdk_client.download_file_from_container(
                        fw_file.parent.id, fw_file.name, file_path
                    )
                try:
                    # Read the file into a dataframe
                    delimiter = get_delimiter(file_path)
                    table_partition_df = pd.read_csv(
                        file_path, delimiter=delimiter, comment="#"
                    )
                # There may be errors in reading the file, log them and continue
                except csv.Error as exc:
                    print(f"CSV Error in reading file: {file_path}")
                    print(exc)
                    continue
                except pd.errors.EmptyDataError as exc:
                    print(f"Empty file: {file_path}")
                    print(exc)
                    continue
                except pd.errors.ParserError as exc:
                    print(f"Parser error: {file_path}")
                    print(exc)
                    continue
                except Exception as exc:
                    print(f"Error reading file: {file_path}")
                    print(exc)
                    continue

                # Add parent information to the table for this file
                table_partition_df = add_parent_info(
                    table_partition_df, fw_file.to_dict()
                )

                # TODO: Saving with pyarrow.parquet.write_table is more efficient and
                # gives the ability to "evolve" the schema. It would eliminate the need
                # to enforce the schema on the table.
                # Enforce the schema on the table
                schema_model = DataModel(**schema_to_save)
                table_partition_df = enforce_field_types(
                    schema_model, table_partition_df, enforce=True
                )

                # Save the table partition to the dataset directory
                save_table(
                    self.dataset_path,
                    schema_name,
                    table_partition_df,
                    partition=fw_file.file_id,
                )

            # If the table directory does not exists or is empty
            # remove the directory and the schema file
            table_path = self.dataset_path / "tables" / schema_name
            schema_path = self.dataset_path / "schemas" / f"{schema_name}.json"
            if not table_path.exists():
                schema_path.unlink()
            elif not list(table_path.glob("*")):
                table_path.rmdir()
                schema_path.unlink()

    def populate_from_tabular_data(self) -> None:
        """Populate the dataset from tabular data referred to in the files table."""

        if not validate_dataset_table(self.duckdb_conn, self.dataset_path, "files"):
            print(
                'The dataset is not valid. The dataset must have a non-empty "files" table.'
            )
            return

        # Filter the files table for tabular data files
        SQL = (
            "SELECT * FROM files where type='tabular data' "
            "ORDER BY file_id, version DESC;"
        )
        results = self.duckdb_conn.execute(SQL)
        # Fetch the files in chunks to avoid memory issues
        # chuck size is given by duckdb.__standard_vector_size__ = 2048
        while not (tab_files_df := results.fetch_df_chunk()).empty:
            # iterate through the filtered files to infer and match schemas
            for _, row in tab_files_df.iterrows():
                # Ensure that the file is downloaded in a hierarchy to avoid naming and
                # path collisions
                # NOTE: If I can retrieve at most 1000 rows at a time for schema
                # creation from a dataview, I can avoid downloading the file. Then I can
                # use a dataview to download the contents of the file to a dataframe and
                # then to a parquet dataset. This would avoid the need to download the
                # file to the local filesystem. This may also be applicable to non-csv
                # files that this code is not currently handling.
                fw_file = self.sdk_client.get_file(row["file_id"])
                file_path = self.files_cache_path / get_container_path(fw_file)
                file_path = file_path / row["name"]
                if not file_path.exists():
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    self.sdk_client.download_file_from_container(
                        fw_file.parent_ref.id, fw_file.name, file_path
                    )

                # Attempt to match the schema of the file with existing schemas
                try:
                    schema = get_table_schema(file_path)
                    matched_schema_key = match_table_schema(
                        self.schema_mappings, schema
                    )
                except ValueError as exc:
                    print(f"Error matching schema for {row['name']}")
                    print(exc)
                    continue

                row_file_record = {"file_id": row.file_id, "name": row["name"]}
                if matched_schema_key:
                    # If a match is found, add the file to the matched schema
                    self.schema_mappings[matched_schema_key]["files"].append(
                        row_file_record
                    )
                else:
                    # If no match is found, create a new schema
                    schema["files"] = [row_file_record]

                    schema["description"] = (
                        f"Table derived from Tabular Data File: {row['name']}"
                    )
                    # Save the schema to the matched_schemas dictionary
                    # Use the file name without the extension
                    self.schema_mappings[file_path.stem] = schema

        # Save the matched schemas and the referenced files to the dataset directory
        self.save_schema_mappings()
