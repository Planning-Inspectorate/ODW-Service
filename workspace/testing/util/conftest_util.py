from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential
import workspace.testing.util.constants as constants
import os


class ConftestUtil():
    @classmethod
    def get_credential_endpoint(cls) -> str:
        endpoint = os.getenv(constants.CREDENTIAL_ENVIRONMENT_NAME)
        if endpoint is None:
            endpoint = constants.CREDENTIAL_ENVIRONMENT_DEFAULT
        print(f"Credential Name is {endpoint}")
        return endpoint

    @classmethod
    def get_synapse_endpoint(cls) -> str:
        endpoint = os.getenv(constants.SYNAPSE_ENDPOINT_ENVIRONMENT_VARIABLE)
        if endpoint is None:
            endpoint = constants.SYNAPSE_ENDPOINT_DEFAULT
        print(f"Synapse Endpoint is {endpoint}")
        return endpoint

    @classmethod
    def get_azure_credential(cls, client_id: str, client_secret: str, tenant_id: str):
        if client_id is None or client_secret is None or tenant_id is None:
            print(f"Credentials created from default")
            credentials = DefaultAzureCredential()
            return credentials
        print(f"Credentials created from parameters ")
        credentials = ClientSecretCredential(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id
        )
        return credentials
