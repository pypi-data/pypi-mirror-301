from azure.identity import AzureCliCredential
from azure.storage.blob import BlobServiceClient, ContainerClient

from btpy.configuration.config import get_env_data_storage_name

_blob_service_client = None


def get_azure_credential():
    return AzureCliCredential()
    # return DefaultAzureCredential()


def to_azure_appsetting_format(setting_value: str) -> str:
    return setting_value.replace(":", "__")


def from_azure_appsetting_format(setting_value: str) -> str:
    return setting_value.replace("__", ":")


def get_blob_service_client() -> BlobServiceClient:
    global _blob_service_client

    if _blob_service_client is None:
        credential = get_azure_credential()
        blob_account_url = f"https://{get_env_data_storage_name()}.blob.core.windows.net"
        _blob_service_client = BlobServiceClient(blob_account_url, credential=credential)

    return _blob_service_client


def get_blob_container_client(container_name: str) -> ContainerClient:
    blob_service_client = get_blob_service_client()
    return blob_service_client.get_container_client(container_name)


def get_blob_client(container_name: str, blob_name: str):
    container_client = get_blob_container_client(container_name)
    return container_client.get_blob_client(blob_name)


def to_blob_index_format(tag: str) -> str:
    return tag.replace("-", "_")
