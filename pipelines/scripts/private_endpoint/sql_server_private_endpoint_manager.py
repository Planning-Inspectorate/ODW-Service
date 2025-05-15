from pipelines.scripts.private_endpoint.private_endpoint_manager import PrivateEndpointManager
from azure.mgmt.synapse import SynapseManagementClient
from typing import List, Type


class SSQLServerPrivateEndpointManager(PrivateEndpointManager):
    def get_resource_type(self):
        return "Microsoft.Sql/servers"
