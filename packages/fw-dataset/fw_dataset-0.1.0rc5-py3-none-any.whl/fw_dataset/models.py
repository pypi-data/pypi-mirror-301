import json
import warnings
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import duckdb
import pyarrow.dataset as ds
from duckdb import DuckDBPyConnection
from pydantic import AnyUrl, BaseModel, Field
from pydantic.main import IncEx

from .filesystem_fns import get_storage_filesystem

# NOTE: The following models are based on the GA4GH Data Connect API specification.
#       They are reused and adapted for the purposes of the Flywheel Dataset Client.

# Suppress specific warning related to shadowing
warnings.filterwarnings(
    "ignore",
    message='Field name "schema" in "DataModel" shadows an attribute in parent "BaseModel"',
)


class Error(BaseModel):
    """Error object"""

    source: Optional[str]
    title: str
    detail: Optional[str]


class ErrorList(BaseModel):
    """List of errors encountered"""

    items: List[Error]


class DataModel(BaseModel):
    """Data Model describe attributes of Tables.

    The `properties` field is a dictionary where the keys are the names of the columns

    The `required` field is a list of the names of the columns that are required to be
    present in the data.

    The Data Model format follows JSON-Schema Draft 7.
    """

    schema: AnyUrl = Field(
        AnyUrl("http://json-schema.org/draft-07/schema#"), alias="$schema"
    )
    id: Optional[str] = Field(..., alias="$id")
    description: Optional[str] = ""
    properties: Dict[str, Any] = {}
    required: List[str] = []
    type: str = "object"

    class Config:
        populate_by_name: bool = True


class Table(BaseModel):
    """Uniquely identifies a table within this Data Connect service.

    Table names should be human-readable and will typically (but not necessarily)
    be split into two or three parts separated by a dot (`.`).
    """

    name: str
    description: str = ""
    data_model: DataModel
    errors: Optional[ErrorList] = None


class DatasetPaths(BaseModel):
    """Paths for a dataset."""

    root_path: Path = None
    dataset_path: Path = None
    latest_version_path: Path = None
    schemas_path: Path = None
    tables_path: Path = None
    provenance_path: Path = None


class Dataset(BaseModel):
    """A dataset is a collection of tables and schemas."""

    # TODO: `version` should be a mandatory field.
    id: str
    name: str
    description: str = ""
    dataset_info: Dict[str, Any] = {}
    _fs: Any = None  # Filesystem is a private attribute
    fully_populate: bool = True
    conn: Any = None  #  OLAP connection
    tables: Dict[str, Any] = {}
    errors: Optional[list] = None
    paths: DatasetPaths = DatasetPaths()

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        """Dump the model without unserializable attributes.

        This is an override of the Pydantic BaseModel method to exclude non-serializable
        and unessential attributes from the dump.

        TODO: Create simplified models for serialization.

        Args:
            mode (str, optional): The dumping mode. Defaults to "json".

        Returns:
            Dict: A JSON-serializable dictionary.
        """
        arguments = {
            "mode": mode,
            "include": include,
            "exclude": exclude,
            "context": context,
            "by_alias": by_alias,
            "exclude_unset": exclude_unset,
            "exclude_defaults": exclude_defaults,
            "exclude_none": exclude_none,
            "round_trip": round_trip,
            "warnings": warnings,
            "serialize_as_any": serialize_as_any,
        }
        # Enumerate attributes to backup
        backup_attr = [
            "conn",
            "_fs",
            "dataset_info",
            "tables",
            "paths",
        ]
        backups = {}
        for attr in backup_attr:
            backups[attr] = getattr(self, attr)
            setattr(self, attr, None)

        self.dataset_info = {}
        self.tables = {}

        dump_json = super().model_dump(**arguments)

        # Restore attributes from backup
        for attr in backup_attr:
            setattr(self, attr, backups[attr])

        return dump_json

    def get_olap_connection(self):
        """Connect to the OLAP database.

        TODO: Add support for other OLAP databases or Cloud OLAP services.
        """
        if not self.conn:
            # Initialize OLAP connection
            # TODO: Create configurations that allow chdb, starrocks, etc.
            self.conn = duckdb.connect()

    def setup_paths(self):
        """Setup the paths for the dataset."""
        self.paths.root_path = Path(self.dataset_info["bucket"])
        self.paths.dataset_path = self.paths.root_path / self.dataset_info["prefix"]
        self.paths.latest_version_path = self.paths.dataset_path / "versions/latest"
        self.paths.schemas_path = self.paths.latest_version_path / "schemas"
        self.paths.tables_path = self.paths.latest_version_path / "tables"
        self.paths.provenance_path = self.paths.latest_version_path / "provenance"

    def get_table_schema(self, table_name: str) -> Table:
        """Load the schema for a table.

        Args:
            table_name (str): The name of the table to load the schema for.

        Returns:
            Table: The table object with the schema loaded.
        """
        schema_path = self.paths.schemas_path / f"{table_name}.schema.json"
        schema = json.loads(self._fs.read_text(schema_path))
        return Table(
            name=table_name,
            description=schema.get("description", ""),
            data_model=DataModel(**schema),
        )

    def initialize_table_schemas(self):
        """Initialize the schemas for all the tables."""
        schema_search_str = str(self.paths.schemas_path / "*.schema.json")
        table_names = [
            Path(table).name.split(".")[0] for table in self._fs.glob(schema_search_str)
        ]
        for table_name in table_names:
            # TODO: Give status bar update on the registration of the tables.
            table = self.get_table_schema(table_name)
            self.tables[table.name] = table

    def register_virtual_table(self, table):
        """Register a virtual table with the OLAP connection.

        Args:
            table (Table): The table object to register the parquet files as a virtual table.
        """
        table_path = self.paths.tables_path / table.name
        if self.dataset_info["type"] in ["fs", "local"]:
            filesystem = None
        else:
            filesystem = self._fs
        dataset = ds.dataset(str(table_path), filesystem=filesystem)
        scanner = ds.Scanner.from_dataset(dataset)
        self.conn.register(table.name, scanner)

    def populate_tables(self):
        """Populate the tables with the data from the filesystem.

        TODO: Add support for other file formats and data sources.
        """
        for table_name, table in self.tables.items():
            if self._fs.exists(self.paths.tables_path / table_name):
                self.register_virtual_table(table)

    def connect(self, fully_populate: bool = True) -> DuckDBPyConnection:
        """Connect to the OLAP database and populate the tables.

        TODO: Add support for other OLAP databases or Cloud OLAP services.

        Args:
            fully_populate (bool, optional): Fully populate the tables. Defaults to True.

        Returns:
            DuckDBPyConnection: A connection to the OLAP database.
        """
        # Make retrieving the storage_creds entirely transient
        self.fully_populate = fully_populate
        self.setup_paths()
        self.get_olap_connection()
        self.initialize_table_schemas()
        if fully_populate:
            self.populate_tables()
        return self.conn

    def execute(self, query: str) -> DuckDBPyConnection:
        """Execute a query on the OLAP database.

        Args:
            query (str): A SQL query to execute.

        Raises:
            ValueError: If no OLAP connection is found.

        Returns:
            DuckDBPyConnection: The results from the query.
        """
        if not self.conn:
            raise ValueError("No OLAP connection found")
        return self.conn.execute(query)

    @classmethod
    def get_dataset_from_filesystem(
        cls, fs_type, bucket, prefix, credentials
    ) -> "Dataset":
        """Create a dataset object from an authenticated filesystem.

        Fileystem Types are "s3", "gs", "az", "fs" (local).

        credentials must be a dictionary with a url key for the credential string in the
        following format for each filesystem type:
        {'url': 's3://{bucket}?access_key_id={access_key_id}&secret_access_key={secret_access_key}'}
        {'url': 'gs://{bucket}?application_credentials={
            "type": "service_account",
            "project_id": "{project_id}",
            "private_key_id": "{private_key_id}",
            "private_key": "{private_key}",
            "client_email": "{email}",
            "client_id": "{client_id}",
            "auth_uri":"{auth_uri}",
            "token_uri":"{token_uri}",
            "auth_provider_x509_cert_url":"{auth_provider_x509_cert_url}",
            "client_x509_cert_url":"{client_x509_cert_url}",
            "universe_domain": "googleapis.com"
            }'
        }
        {'url': 'az://{account_name}.blob.core.windows.net/{container}?access_key={access_key}'}

        Args:
            fs_type (str): The type of filesystem to use. Options are "s3", "gs", "az", "fs".
            bucket (str): The bucket, container, or root directory of the dataset.
            prefix (str): The path from the bucket to the dataset.
            credentials (dict): A dictionary with a url key for the credential string.

        Returns:
            Dataset: A dataset object.
        """
        # Create the filesystem with the credentials and we discard the credentials
        filesystem = get_storage_filesystem(fs_type, credentials)

        # build the path to the latest version of the dataset
        dataset_path = Path(f"{bucket}/{prefix}")
        latest_version_path = dataset_path / "versions/latest"
        dataset_description_path = (
            latest_version_path / "provenance" / "dataset_description.json"
        )

        # load the dataset description from the filesystem
        dataset_description = json.loads(filesystem.read_text(dataset_description_path))

        # instantiate the dataset object from the dataset description
        dataset = Dataset(**dataset_description)

        # set the filesystem and dataset info
        dataset.dataset_info = {"bucket": bucket, "prefix": prefix, "type": fs_type}
        dataset._fs = filesystem

        return dataset
