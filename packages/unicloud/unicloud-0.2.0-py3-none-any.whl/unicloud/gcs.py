""" This module is responsible for creating a GCS client """
from typing import Optional
from pathlib import Path
import os
import base64
import json
from unicloud.abstract_class import CloudStorageFactory
from google.oauth2 import service_account
from google.cloud import storage
from unicloud.secret_manager import decode


class GCS(CloudStorageFactory):
    """GCS Cloud Storage"""

    def __init__(self, project_name: str, service_key: Optional[str] = None):
        """
        Initializes the GCS client.

        Parameters
        ----------
        project_name: [str]
            The Google Cloud project name.
        service_key: [str]
            The path to your service key file.
        """
        self._project_id = project_name
        if service_key is not None:
            if not Path(service_key).exists():
                raise FileNotFoundError(
                    f"The service key file {service_key} does not exist"
                )

        self.service_key = service_key
        self._client = self.create_client()

    @property
    def project_id(self):
        """project_id."""
        return self._project_id

    @property
    def client(self):
        """client."""
        return self._client

    def create_client(self) -> storage.client.Client:
        """create_client.

            the returned client deals with everything related to the specific project. For Google Cloud Storage,

            authenticating via a service account is the recommended approach. If you're running your code on a Google
            Cloud environment (e.g., Compute Engine, Cloud Run, etc.), the environment's default service account
            might automatically be used, provided it has the necessary permissions. Otherwise, you can set the
            GOOGLE_APPLICATION_CREDENTIALS environment variable to point to your service account JSON key file.

        Returns
        -------
        google cloud storage client object
        """
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            credentials = service_account.Credentials.from_service_account_file(
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            )
            client = storage.Client(project=self.project_id, credentials=credentials)
            # client = storage.Client(project=self.project_name)
        elif "SERVICE_KEY_CONTENT" in os.environ:
            # key need to be decoded into a dict/json object
            service_key_content = decode(os.environ['SERVICE_KEY_CONTENT'])

            service_key_content = json.loads(service_key_content)
            # connection to the service account
            client = storage.Client.from_service_account_info(service_key_content)
        elif self.service_key:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_key
            )
            client = storage.Client(project=self.project_id, credentials=credentials)
        else:
            raise ValueError(
                "Since the GOOGLE_APPLICATION_CREDENTIALS and the EE_PRIVATE_KEY and EE_SERVICE_ACCOUNT are not in your"
                "env variables you have to provide a path to your service account"
            )

        return client

    def upload(self, file_path: str, destination: str):
        """Upload a file to GCS.

        Parameters
        ----------
        file_path: [str]
            The path to the file to upload.
        destination: [str]
            The destination path in the cloud storage.
        """
        bucket_name, object_name = destination.split("/", 1)
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to {destination}.")

    def download(self, source, file_path):
        """Download a file from GCS.

        Parameters
        ----------
        source: [str]
            The source path in the cloud storage.
        file_path: [str]
            The path to save the downloaded file.
        """
        bucket_name, object_name = source.split("/", 1)
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.download_to_filename(file_path)
        print(f"File {source} downloaded to {file_path}.")
