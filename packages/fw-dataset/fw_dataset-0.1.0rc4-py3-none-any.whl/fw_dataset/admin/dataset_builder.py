"""Module to build a dataset from a Flywheel project."""

import gzip
import shutil
import sqlite3
import time
from pathlib import Path
from typing import Dict

import orjson as json
import pandas as pd
from flywheel import Client as SDKClient
from fw_client import FWClient as APIClient

from ..constants import (
    DATAHOME,
    INFO_SCHEMA,
    POPULATE_CUSTOM_INFO,
    POPULATE_TABULAR_DATA,
    SNAPSHOT_MAPPINGS,
    SNAPSHOT_TIMEOUT,
    TABLES,
)
from ..exceptions import SnapshotCreationError
from .admin_helpers import save_custom_info_table, save_schema, save_table
from .custom_info_table_builder import CustomInfoTableBuilder
from .tabular_file_table_builder import TabularFileTableBuilder


class DatasetBuilder:
    """Class to build a dataset from a Flywheel project."""

    def __init__(
        self,
        api_key: str,
        dataset_id: str,
        label: str | None = None,
        description: str | None = None,
    ) -> None:
        """Initialize the dataset object.flywheel.Client.

        Assign the Flywheel client, dataset ID, label, and description to the dataset.

        An SDK client is instantiated from the API Client.

        Args:
            api_key (str): The Flywheel API Key to initialize api and sdk clients.
            dataset_id (str): The dataset ID.
            label (str, optional): The label of the dataset. Defaults to None.
            description (str, optional): The description of the dataset. Defaults to None.
        """
        self.api_key = api_key
        # TODO: Check if the API key is valid, if not raise an error
        self.sdk_client = SDKClient(self.api_key)
        self.api_client = APIClient(api_key=self.api_key)
        self.dataset_id = dataset_id
        # TODO: check if the project exists... if not, raise an error
        self.project = self.sdk_client.get(dataset_id).reload()
        self.partition_size = 10_000  # TODO: Make this a parameter in constants.py

        if not label:
            label = self.project.label

        if not description:
            description = self.project.description

        self.label = label
        self.description = description
        self.instance_address = self.api_client.config.baseurl.split("/")[-1]

        # TODO: Implement a method to allow the user to specify DATAHOME as parameter
        self.dataset_path = DATAHOME / self.instance_address / dataset_id

        # Create the dataset directory
        self.dataset_path.mkdir(parents=True, exist_ok=True)

        # Create a directory to store the cached tabular data and custom info files
        self.files_cache_path = self.dataset_path / "temp_file_cache"
        self.files_cache_path.mkdir(parents=True, exist_ok=True)

        # Initialize the tables dictionary to store the container dataframe partitions
        self.tables = {}

    @classmethod
    def is_populated(cls, instance_address, dataset_id) -> bool:
        """Check if the dataset is populated.

        Returns:
            bool: True if the dataset is populated, False otherwise.
        """
        dataset_path = DATAHOME / instance_address / dataset_id

        for table in TABLES:
            # Check for the existence of the schema
            if not (dataset_path / f"schemas/{table['id']}.json").exists():
                return False
            # Check for the existence of the table
            table_path = dataset_path / f"tables/{table['id']}/"
            if not table_path.exists():
                return False
            # Check for the existence of the parquet files for the table
            parquet_files = list(table_path.glob("*.parquet"))
            if not parquet_files:
                return False

        # Check for the existence of the project record
        if not (dataset_path / "project.json.gz").exists():
            return False

        return True

    def create_snapshot(self) -> Dict:
        """Create a snapshot of the dataset and wait for it to complete.

        Snapshots have the following statuses:
        - "pending"
        - "in_progress"
        - "complete"
        - "failed"

        TODO: Make this asynchronous and use a callback to notify the user when it is
        complete.

        Returns:
            Dict: The snapshot of the dataset.
        """
        start_creation = time.time()
        snapshot = self.api_client.post(
            f"/snapshot/projects/{self.dataset_id}/snapshots"
        )
        while snapshot and snapshot["status"] != "complete":
            time.sleep(10)
            response = self.api_client.get(
                f"/snapshot/projects/{self.dataset_id}/snapshots"
            )
            if not response:
                raise SnapshotCreationError("Snapshot creation failed.")

            snapshot = response[-1]
            creation_time = time.time() - start_creation
            if creation_time > SNAPSHOT_TIMEOUT or snapshot["status"] == "failed":
                raise SnapshotCreationError("Snapshot creation timed out or failed.")
        return snapshot

    def create_or_get_latest_snapshot(self, force_new: bool = False) -> None:
        """Create or get the latest snapshot of the dataset.

        Args:
            force_new (bool, optional): Force the creation of a new snapshot. Defaults
            to False.

        Returns:
            None
        """

        # Check if a snapshot exists, if not create one
        snapshots = self.api_client.get(
            f"/snapshot/projects/{self.dataset_id}/snapshots"
        )

        # TODO: Save the snapshot record to the dataset directory
        if not snapshots or force_new:
            self.snapshot = self.create_snapshot()
        else:
            self.snapshot = snapshots[-1]

    def decompress_snapshot(self) -> Path:
        """Decompress the snapshot of the dataset."""
        snapshot_id = self.snapshot["_id"]

        # Write the snapshot record to a file
        with open(self.files_cache_path / "snapshot_info.json", "w") as f:
            f.write(json.dumps(self.snapshot, default=str).decode("utf-8"))

        # TODO: Is there a way to stream the download directly to the decompression
        # step? Or directly to a file? This would save RAM.
        resp = self.api_client.get(
            f"/snapshot/projects/{self.dataset_id}/snapshots/{snapshot_id}", stream=True
        )
        # TODO: Check the date of the snapshot and only download if it is newer
        snapshot_file_path = self.files_cache_path / "snapshot.db.gz"
        decompressed_path = self.files_cache_path / "snapshot.db"

        with open(snapshot_file_path, "wb") as fp:
            fp.write(resp.content)

        # Decompress the downloaded file.
        with gzip.open(snapshot_file_path, "rb") as f_in, open(
            decompressed_path, "wb"
        ) as f_out:
            shutil.copyfileobj(f_in, f_out)

        # Remove the compressed files
        snapshot_file_path.unlink()

        return decompressed_path

    def extract_custom_info_from_container_records(
        self, container_records: list, container_type: str
    ) -> pd.DataFrame:
        """Extract custom information from container records.

        Args:
            container_records (list): List of container records as dictionaries.
            container_type (str): The type of container.

        Returns:
            pd.DataFrame: A DataFrame containing the custom information.
        """
        # Initializing the custom_info_df to the INFO_SCHEMA properties
        columns_list = list(INFO_SCHEMA.properties.keys())
        empty_custom_info_df = pd.DataFrame(columns=columns_list)
        custom_info_file_list = []
        for row in container_records:
            if custom_info := row.get("info"):
                if container_type == "file":
                    container_id = row["_id"].get("file_id")
                else:
                    container_id = row["_id"]
                # Remove the custom info from the row
                row.pop("info")

                # Save the custom info to a string
                cust_info_payload = json.dumps(custom_info)

                custom_info_record = {
                    f"parents.{key}": value for key, value in row["parents"].items()
                }
                custom_info_record[f"parents.{container_type}"] = container_id
                custom_info_record["custom_info"] = cust_info_payload
                custom_info_file_list.append(custom_info_record)

        tmp_df = pd.DataFrame(custom_info_file_list)
        if self.tables.get("custom_info") is None:
            return pd.concat([empty_custom_info_df, tmp_df])
        else:
            return pd.concat([self.tables["custom_info"], tmp_df])

    def save_table_to_dataset(
        self, table: str, table_name: str, raw_list: list, table_columns: list
    ) -> None:
        """Save a table partition to the dataset directory.

        Args:
            table (str): The type of table.
            table_name (str): The name of the table.
            raw_list (list): The list of dictionaries to save.
            table_columns (list): The columns of the table.
        """
        # Ensure we have all the columns in the table
        temp_df = pd.DataFrame(columns=table_columns)
        table_df = pd.json_normalize(raw_list)

        # Rename the columns to match the schema
        field_mappings = SNAPSHOT_MAPPINGS[table]["field_mappings"]
        table_df = table_df.rename(columns=field_mappings)

        # Ensure all columns exist and are in the correct order
        table_df = pd.concat([temp_df, table_df])
        table_df = table_df[table_columns]

        table_schema = SNAPSHOT_MAPPINGS[table]["schema"]

        save_schema(self.dataset_path, table_name, table_schema.model_dump(mode="json"))

        # TODO: We may want to repartition the tables based on column values
        # NOTE: pyarrow can be used to write the parquet files with partitioning
        #       from an individual dataframe
        partition_name = table_df.iloc[0].get("id") if not table_df.empty else table
        save_table(self.dataset_path, table_name, table_df, partition=partition_name)

    def load_tables_from_snapshot(self) -> None:
        """Load data from the latest snapshot of the dataset."""
        # Decompress the snapshot
        snapshot_file_path = self.decompress_snapshot()
        conn = sqlite3.connect(snapshot_file_path)

        snapshot_tables = ["subject", "session", "acquisition", "file", "analysis"]

        # There is only one project record in the snapshot
        _, project_results = conn.execute("SELECT * FROM project").fetchone()

        project_dict = json.loads(project_results)

        self.tables["custom_info"] = self.extract_custom_info_from_container_records(
            [project_dict], "project"
        )

        # save the project record to a gzipped json file at the dataset level
        # TODO: Implement the display of the project record in the dataset UI
        with gzip.open(self.dataset_path / "project.json.gz", "wb") as f:
            f.write(json.dumps(project_dict, default=str))

        # Loop through the database tables and load them into the dataset object
        for table in snapshot_tables:
            table_columns = SNAPSHOT_MAPPINGS[table]["schema"].properties.keys()
            table_name = SNAPSHOT_MAPPINGS[table]["table_name"]

            # Iterate through the table in partition_size chunks
            for raw_df in pd.read_sql_query(
                f"SELECT * FROM {table}", conn, chunksize=self.partition_size
            ):
                # Convert the raw data to a list of dictionaries
                raw_list = [json.loads(row) for row in raw_df.data.values]

                # Extract the custom information from the container records
                self.tables["custom_info"] = (
                    self.extract_custom_info_from_container_records(
                        raw_list, container_type=table
                    )
                )

                self.save_table_to_dataset(table, table_name, raw_list, table_columns)

                # Custom Information is a "hidden" table that is not displayed in the UI
                # It is used to store the custom information of the containers for later
                # extraction into tables for fast querying
                if self.tables["custom_info"].shape[0] >= self.partition_size:
                    self.tables["custom_info"] = save_custom_info_table(
                        self.dataset_path, self.tables["custom_info"]
                    )

        self.tables["custom_info"] = save_custom_info_table(
            self.dataset_path, self.tables["custom_info"]
        )

    def populate_dataset(
        self,
        parse_tabular_data: bool = POPULATE_TABULAR_DATA,
        parse_custom_info: bool = POPULATE_CUSTOM_INFO,
        remove_temp_files: bool = True,
    ) -> Path | None:
        """Populate a dataset from a Flywheel project id.

        This function creates a dataset from a Flywheel project by creating and
        populating the following containers as tables from a snapshot:
        - Subjects
        - Sessions
        - Acquisitions
        - Analyses
        - Files

        Optionally, tabular data and custom information can be parsed into tables. As
        this can take a long time, it is disabled by default.

        Args:
            project_id (str): The Flywheel project ID to create the dataset from.
            parse_tabular_files (bool, optional): Parse Tabular Files to tables . Defaults to POPULATE_TABULAR_DATA.
            parse_custom_info (bool, optional): Parse custom info to tables. Defaults to POPULATE_CUSTOM_INFO.
            remove_temp_files (bool, optional): Remove temp files after complete. Defaults to True.
        Returns:
            Path: The path to the dataset.
        """
        try:
            self.create_or_get_latest_snapshot()
            self.load_tables_from_snapshot()

            # Parse tabular data files only if specified
            if parse_tabular_data:
                tabular_file_table_builder = TabularFileTableBuilder(
                    self.dataset_path, self.files_cache_path, self.sdk_client
                )
                tabular_file_table_builder.populate_from_tabular_data()

            # Parse custom information only if specified
            if parse_custom_info:
                # Search hidden "custom_info" table for file info with "qc" and "header"
                # tags at top level
                custom_info_table_builder = CustomInfoTableBuilder(self.dataset_path)
                custom_info_table_builder.populate_from_custom_information()

            if remove_temp_files:
                shutil.rmtree(self.files_cache_path)

        except Exception as e:
            print(f"Error rendering snapshot: {e}")
            return None
        else:
            return self.dataset_path
