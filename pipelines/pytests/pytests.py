import pytest
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

@pytest.fixture(scope="module")
def azure_client():
    credential = DefaultAzureCredential()
    subscription_id = 'ff442a29-fc06-4a13-8e3e-65fd5da513b3'
    return ResourceManagementClient(credential, subscription_id)

def test_resource_group_exists(azure_client):
    rg_name = 'pins-rg-devops-odw-dev-ukw'
    resource_group = azure_client.resource_groups.get(rg_name)
    assert resource_group is not None, f"Resource group '{rg_name}' does not exist"
