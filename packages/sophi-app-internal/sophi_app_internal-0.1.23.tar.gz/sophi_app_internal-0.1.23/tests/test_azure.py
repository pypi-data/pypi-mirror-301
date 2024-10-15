import pytest
from cryptography.fernet import Fernet

from sophi_app_internal.Intergrations.Microsoft.azure import UserAzureBlobStorage


def test_encryption():
    blob_storage = UserAzureBlobStorage("test")
    blob_storage.upload_file(b"test", "test", overwrite=True)
    res = blob_storage.download_file("test").readall()
    assert res == b"test"

    secure_upload = blob_storage.upload_file_secure(b"test", "test", overwrite=True)

    res = blob_storage.download_file("test").readall()
    assert res != b"test"

    key = secure_upload["encryption_key"]

    fernet = Fernet(key)
    assert fernet.decrypt(res) == b"test"

    assert blob_storage.download_file_secure("test", key) == b"test"
    blob_storage.delete_all_blobs()


if __name__ == "__main__":
    pytest.main([__file__])
