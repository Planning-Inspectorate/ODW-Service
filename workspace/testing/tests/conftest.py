import pytest
import datetime
import pytest
import pyodbc
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import constants
from azure.storage.filedatalake import DataLakeServiceClient


def pytest_addoption(parser):
    # synapse name
    parser.addoption("--synapse", action="store",
                     default="pins-synw-odw-dev-uks")
    # pipeline name
    parser.addoption("--pipeline", action="store",
                     default="MasterPipeline")

    # input location at landing zone
    parser.addoption("--client_id", action="store")
    # input location at landing zone
    parser.addoption("--client_secret", action="store")
    # input location at landing zone
    parser.addoption("--tenant", action="store")

@pytest.fixture()
def input_sample_file_name(pytestconfig) -> str:
    return pytestconfig.getoption("input_sample_filename")

@pytest.fixture()
def pipeline_name(pytestconfig) -> str:
    return pytestconfig.getoption("pipeline")

@pytest.fixture()
def container_name(pytestconfig) -> str:
    return pytestconfig.getoption("container_name")

@pytest.fixture()
def file_time(pytestconfig) -> datetime:
    return datetime.datetime.now()

@pytest.fixture()
def synapse_endpoint(pytestconfig) -> str:
    synapse_name = pytestconfig.getoption("synapse")
    endpoint = f"https://{synapse_name}.dev.azuresynapse.net"
    return endpoint

@pytest.fixture()
def azure_credential(pytestconfig):
    client_id = pytestconfig.getoption("client_id")
    client_secret = pytestconfig.getoption("client_secret")
    tenant_id = pytestconfig.getoption("tenant")
    if client_id is None or client_secret is None or tenant_id is None:
        print(f"###########Credentials created from default")
        credentials = DefaultAzureCredential()
        return credentials
    else:
        print(f"########### Credentials created from parameters ")
        credentials = ClientSecretCredential(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id)
        return credentials