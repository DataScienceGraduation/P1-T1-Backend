from azure.storage.blob import BlobServiceClient
from django.core.files.storage import Storage
from django.conf import settings

class AzureBlobStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.azure_storage_connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
        self.container_name = settings.AZURE_CONTAINER

    def _open(self, name, mode='rb'):
        blob_service_client = BlobServiceClient.from_connection_string(self.azure_storage_connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=name)
        file_contents = blob_client.download_blob().readall()
        return ContentFile(file_contents)

    def _save(self, name, content):
        blob_service_client = BlobServiceClient.from_connection_string(self.azure_storage_connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=name)
        blob_client.upload_blob(content.read(), overwrite=True)
        return name

    def url(self, name):
        return f"https://{settings.AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{self.container_name}/{name}"

    def deconstruct(self):
        return 'urbanbackend.custom_storage.AzureBlobStorage', [], {}

    def exists(self, name):
        blob_service_client = BlobServiceClient.from_connection_string(self.azure_storage_connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=name)
        return blob_client.exists()
