from pipelines.scripts.private_endpoint.private_endpoint_manager import PrivateEndpointManager
from azure.mgmt.synapse import SynapseManagementClient
from typing import List, Type


class SynapsePrivateEndpointManager(PrivateEndpointManager):
    def get_client_class(cls) -> Type:
        return SynapseManagementClient

    def get_required_kwargs(cls) -> List[str]:
        return [
            "workspace_name",
            "resource_group_name"
        ]

    def get_optional_kwargs(cls) -> List[str]:
        return []
