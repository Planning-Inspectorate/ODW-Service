from pipelines.scripts.private_endpoint.private_endpoint_manager import PrivateEndpointManager
from pipelines.scripts.util import Util
from azure.mgmt.synapse import SynapseManagementClient
from typing import List, Dict, Any


class SynapsePrivateEndpointManager(PrivateEndpointManager):
    def __init__(self, subscription_id: str, resource_group: str):
        synapse_management_client = SynapseManagementClient()

    def get_private_endpoint(self, private_endpoint_name: str, **kwargs: str) -> Dict[str, Any]:
        if synapse_name not in kwargs:
            raise ValueError(f"Expected `synapse_name` to be passed to SynapsePrivateEndpointManager.get_private_endpoint")
        if resource_group_name not in kwargs:
            raise ValueError(f"Expected `resource_group_name` to be passed to SynapsePrivateEndpointManager.get_private_endpoint")
        synapse_name = kwargs["synapse_name"]
        resource_group_name = kwargs["resource_group_name"]
        return self.synapse_management_client.private_endpoint_connections.get(
            resource_group_name=resource_group_name,
            workspace_name=synapse_name,
            private_endpoint_connection_name=private_endpoint_name
        ).as_dict()

    def approve_private_endpoint(self, private_endpoint_name: str, **kwargs: str) -> Dict[str, Any]:
        """
            Approve a private endpoint that is pending in a synapse workspace
        """
        if synapse_name not in kwargs:
            raise ValueError(f"Expected `synapse_name` to be passed to SynapsePrivateEndpointManager.get_private_endpoint")
        if resource_group_name not in kwargs:
            raise ValueError(f"Expected `resource_group_name` to be passed to SynapsePrivateEndpointManager.get_private_endpoint")
        synapse_name = kwargs["synapse_name"]
        resource_group_name = kwargs["resource_group_name"]
        existing_endpoint = self.get_synapse_private_endpoint(private_endpoint_name, synapse_name, resource_group_name)
        if existing_endpoint["private_link_service_connection_state"]["status"] == "Approved":
            # Attempting to reapprove causes an error, so abort in this case
            return existing_endpoint
        poller = self.synapse_management_client.private_endpoint_connections.begin_create(
            resource_group_name=resource_group_name,
            workspace_name=synapse_name,
            private_endpoint_connection_name=private_endpoint_name,
            request={
                "properties": {
                    "privateLinkServiceConnectionState": {
                        "description": f"Auto-Approved by {Util.get_user()}",
                        "status": "Approved"
                    }
                }
            }
        )
        poller.wait(300.0)
        return poller.result()

    def get_all(self, **kwargs: str) -> List[Dict[str, Any]]:
        if synapse_name not in kwargs:
            raise ValueError(f"Expected `synapse_name` to be passed to SynapsePrivateEndpointManager.get_private_endpoint")
        if resource_group_name not in kwargs:
            raise ValueError(f"Expected `resource_group_name` to be passed to SynapsePrivateEndpointManager.get_private_endpoint")
        synapse_name = kwargs["synapse_name"]
        resource_group_name = kwargs["resource_group_name"]
        return self.synapse_management_client.private_endpoint_connections.list(
            resource_group_name=resource_group_name,
            workspace_name=synapse_name
        ).as_dict()
