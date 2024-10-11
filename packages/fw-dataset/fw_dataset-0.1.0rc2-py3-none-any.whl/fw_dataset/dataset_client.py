import json
from pathlib import Path

from flywheel import Client as SDKClient
from fw_client import FWClient as APIClient

from .filesystem_fns import get_storage_filesystem
from .models import Dataset


class FWDatasetClient:
    """A Flywheel Dataset Client.

    The FWDatasetClient is a client for interacting with Flywheel datasets. It can be
    used to get a list of datasets in a Flywheel instance, get a dataset object from a
    dataset_id or a path to a dataset, and create a dataset object from an authenticated
    filesystem.
    """

    def __init__(self, api_key: str):
        """Initialize the FWDatasetClient.

        Args:
            api_key (str): The Flywheel API key for the Flywheel instance.
        """
        self.api_key = api_key
        self.sdk_client = SDKClient(api_key)
        self.api_client = APIClient(api_key=api_key)

    def _get_storage_credentials(self, dataset: Dataset) -> dict:
        """Get the storage credentials for a dataset.

        Retrieves the storage credentials for a dataset from the registered storage for
        this dataset and the project it is associated with.

        Args:
            dataset (Dataset): The dataset object.

        Raises:
            ValueError: If Storage credentials are not found for the dataset.
            ValueError: If Storage type mismatch.

        Returns:
            dict: The storage credentials for the dataset.
        """
        dataset_info = dataset.dataset_info
        fs_type = dataset_info.get("type")
        storage_creds = dataset_info.get("credentials")

        if not storage_creds and (storage_id := dataset_info.get("storage_id")):
            storage = self.api_client.get(f"/xfer/storages/{storage_id}")
            storage_creds = self.api_client.get(f"/xfer/storage-creds/{storage_id}")
            if not storage_creds:
                raise ValueError(
                    f"Storage credentials not found for storage_id: {storage_id}"
                )
            if storage["config"]["type"] != fs_type:
                raise ValueError(
                    f"Storage type mismatch: {storage['config']['type']} != {fs_type}"
                )
        elif not storage_creds:
            raise ValueError("Storage credentials not found for dataset")

        return storage_creds

    def datasets(self):
        """Get all datasets in the Flywheel instance.

        Iterates through all projects in the Flywheel instance, checks for a dataset
        object in the project info blob, and creates a dataset object for each dataset.

        The dataset object is as follows:
        project.info = {
          "dataset": {
            "type": "s3",
            "bucket": "bucket_name",
            "prefix": "path/to/dataset",
            "storage_id": "storage_id",
          }

        Returns:
            list: A list of a dataset objects in the Flywheel instance.
        """
        datasets = []
        for project in self.sdk_client.projects():
            project = project.reload()
            if dataset_info := project.info.get("dataset"):
                dataset = Dataset(
                    id=project.id,
                    name=project.label,
                    api_key=self.api_key,
                    dataset_info=dataset_info,
                )
                credentials = self._get_storage_credentials(dataset)
                dataset.dataset_info["credentials"] = credentials
                datasets.append(dataset)
        return datasets

    def get_dataset(self, dataset_id: str = None, path: str = None):
        """Get a dataset object from a dataset_id or a path to a dataset.

        Args:
            dataset_id (str, optional): Project ID. Defaults to None.
            path (str, optional): group/project path to dataset. Defaults to None.

        Raises:
            ValueError: If neither dataset_id or path is provided.

        Returns:
            Dataset: A valid dataset object.
        """
        if dataset_id:
            project = self.sdk_client.get(dataset_id)
        elif path:
            if path.startswith("fw://"):
                stripped_path = path.replace("fw://", "")
            else:
                stripped_path = path
            project = self.sdk_client.lookup(stripped_path)
        else:
            raise ValueError(
                "You must provide either a dataset_id or a path to a dataset"
            )
        dataset_info = project.info.get("dataset")

        dataset = Dataset(
            id=dataset_id,
            name=project.label,
            description=project.description,
            api_key=self.api_key,
            dataset_info=dataset_info,
        )
        dataset.dataset_info["credentials"] = self._get_storage_credentials(dataset)

        return dataset

    def get_dataset_from_filesystem(
        self, fs_type, bucket, prefix, credentials
    ) -> Dataset:
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
        filesystem = get_storage_filesystem(fs_type, credentials)
        dataset_path = Path(f"{bucket}/{prefix}")
        latest_version_path = dataset_path / "versions/latest"
        dataset_description_path = (
            latest_version_path / "provenance" / "dataset_description.json"
        )
        dataset_description = json.loads(filesystem.read_text(dataset_description_path))
        dataset = Dataset(**dataset_description)
        dataset.dataset_info = {
            "bucket": bucket,
            "prefix": prefix,
            "type": fs_type,
            "credentials": credentials,
        }
        dataset.fs = filesystem

        return dataset
