from azure.mgmt.synapse import SynapseManagementClient
from typing import List, Dict, Any


class PrivateEndpointManager():
    def get_private_endpoint(self, private_endpoint_name: str, **kwargs: str) -> Dict[str, Any]:
        pass

    def approve_private_endpoint(self, private_endpoint_name: str, **kwargs: str) -> Dict[str, Any]:
        """
            Approve a private endpoint that is pending on the given Azure resource type
        """
        pass
    
    def get_all(self, **kwargs: str) -> List[Dict[str, Any]]:
        pass
