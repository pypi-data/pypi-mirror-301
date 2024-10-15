from hashlib import md5
import os
from pathlib import Path
from azure.storage.blob import BlobServiceClient, BlobBlock, BlobProperties
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()


class UserAzureBlobStorage:
    def __init__(self, user_id: str, connection_string=None):
        self.connection_string = connection_string or os.getenv(
            "AZURE_DEV_STORAGE_CONNECTION_STRING"
        )
        self.user_id = user_id
        self.container_name = "sophi-app-user-" + md5(str(user_id).encode()).hexdigest()

        self.blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.connection_string,
        )

        self.container_client = self._get_or_create_container()

    def _get_or_create_container(self):
        try:
            container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            container_client.get_container_properties()
        except Exception:
            container_client = self.blob_service_client.create_container(
                self.container_name
            )
        return container_client

    def get_blob_properties(self, blob_name) -> BlobProperties:
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.get_blob_properties()

    def upload_file(self, data, blob_name, overwrite=False):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.upload_blob(data, overwrite=overwrite)

    def upload_file_secure(self, data, blob_name, overwrite=False):
        """Encrypts the data before uploading, and returns the encryption key in the result
        as 'encryption_key'.

        """
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        result = self.upload_file(encrypted_data, blob_name, overwrite=overwrite)
        result["encryption_key"] = key
        return result

    def download_file(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.download_blob()

    def download_file_secure(self, blob_name, encryption_key) -> bytes:
        encrypted_data = self.download_file(blob_name)
        fernet = Fernet(encryption_key)
        return fernet.decrypt(encrypted_data.readall())

    def delete_blob(self, blob_name):
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.delete_blob()

    def delete_all_blobs(self):
        return self.container_client.delete_blobs(
            *self.container_client.list_blob_names()
        )

    async def upload_chunked_blob(self, blob_name, async_chunk_generator):
        blob_client = self.container_client.get_blob_client(blob_name)
        block_list = []
        block_id = 0

        async for chunk in async_chunk_generator:
            block_id_str = str(block_id).zfill(5)
            blob_client.stage_block(block_id=block_id_str, data=chunk)
            block_list.append(BlobBlock(block_id=block_id_str))
            block_id += 1

        blob_client.commit_block_list(block_list)

    def list_blobs(self, name_starts_with=None):
        if name_starts_with:
            return self.container_client.list_blobs(name_starts_with=name_starts_with)
        elif name_starts_with is None:
            return self.container_client.list_blobs()
