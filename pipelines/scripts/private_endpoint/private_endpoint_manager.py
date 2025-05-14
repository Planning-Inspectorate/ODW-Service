from typing import List, Dict, Any, Type
from abc import ABC, abstractmethod
from pipelines.scripts.util import Util


class PrivateEndpointManager(ABC):
    def __init__(self, subscription_id: str, resource_group: str):
        self.management_client = self.get_client_class()(subscription_id, resource_group)

    def get_private_endpoint(self, private_endpoint_name: str, **kwargs: str) -> Dict[str, Any]:
        return self.management_client.private_endpoint_connections.get(private_endpoint_name, **kwargs).as_dict()

    def approve_private_endpoint(self, private_endpoint_name: str, **kwargs: str):
        """
            Approve a private endpoint that is pending on the given Azure resource type
        """
        existing_endpoint = self.get_private_endpoint(private_endpoint_name, **kwargs)
        if existing_endpoint["private_link_service_connection_state"]["status"] == "Approved":
            return
        poller = self.management_client.private_endpoint_connections.begin_create(
            private_endpoint_name,
            **kwargs,
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
        poller.result()
        return

    def get_all(self, **kwargs: str) -> List[Dict[str, Any]]:
        return self.management_client.private_endpoint_connections.list(**kwargs).as_dict()

    @abstractmethod
    def get_client_class(cls) -> Type:
        pass

    @abstractmethod
    def get_required_kwargs(cls) -> List[str]:
        pass

    @abstractmethod
    def get_optional_kwargs(cls) -> List[str]:
        pass
