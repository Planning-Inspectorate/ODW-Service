from azure.identity import AzureCliCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobProperties
from concurrent.futures import ThreadPoolExecutor
from typing import Set
import logging


class StorageUtil():
    def _migrate_blob(self, blob_to_copy: BlobProperties, source_container_client: ContainerClient, target_container_client: ContainerClient):
        logging.info(f"Copying blob '{blob_to_copy.name}' from '{source_container_client.account_name}' to '{target_container_client.account_name}'")
        migration_error = None
        try:
            data = source_container_client.download_blob(blob_to_copy.name)
            target_container_client.upload_blob(blob_to_copy.name, data, blob_type=blob_to_copy.blob_type, metadata=blob_to_copy.metadata, overwrite=True)
        except Exception as e:
            logging.error(f"An error occurred when copying blob '{blob_to_copy.name}'")
            migration_error = e
        if migration_error:
            raise migration_error

    def migrate_between_storage_accounts(self, source: str, target: str, paths_to_ignore = Set[str]):
        source_blob_client = BlobServiceClient(f"https://{source}.blob.core.windows.net/", AzureCliCredential())
        target_blob_client = BlobServiceClient(f"https://{target}.blob.core.windows.net/", AzureCliCredential())
        source_containers = {container.name for container in source_blob_client.list_containers()}
        target_containers = {container.name for container in target_blob_client.list_containers()}
        candidate_containers = target_containers.intersection(source_containers)
        print("common: ", candidate_containers)
        for container in candidate_containers:
            if container == "odw-standardised":
                logging.info(f"Processing container '{container}'")
                source_container_client = source_blob_client.get_container_client(container)
                target_container_client = target_blob_client.get_container_client(container)
                all_blobs_to_migrate = [
                    blob
                    for blob in source_container_client.list_blobs()
                    if not any(path in f"{container}/{blob.name}" for path in paths_to_ignore)
                ]
                all_blobs_to_migrate = [x for x in all_blobs_to_migrate if "." in x.name]
                with ThreadPoolExecutor() as tpe:
                    [
                        thread_response
                        for thread_response in tpe.map(
                            self._migrate_blob,
                            all_blobs_to_migrate,
                            [source_container_client] * len(all_blobs_to_migrate),
                            [target_container_client] * len(all_blobs_to_migrate)
                        )
                        if thread_response
                    ]
                #for blob in all_blobs_to_migrate:
                #    self._migrate_blob(blob, source_container_client, target_container_client)
                    #data = source_container_client.download_blob(blob.name)
                    #target_container_client.upload_blob(blob.name, data, blob_type=blob.blob_type, metadata=blob.metadata)

{'odw-config', 'odw-raw', 'odw-curated', 'backup-logs', 'odw-harmonised', 'odw-standardised'}