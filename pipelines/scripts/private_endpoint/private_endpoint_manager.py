from azure.identity import AzureCliCredential
from typing import List, Dict, Any, Type
from abc import ABC, abstractmethod
from pipelines.scripts.util import Util
import logging

class PrivateEndpointManager(ABC):
    def __init__(self, subscription_id: str):
        self.management_client = self.get_client_class()(AzureCliCredential(), subscription_id)

    def get(self, private_endpoint_name: str, **kwargs: str) -> Dict[str, Any]:
        """
            Return the details of the given private endpoint
        """
        self._validate_arguments(**kwargs)
        return self.management_client.private_endpoint_connections.get(private_endpoint_connection_name=private_endpoint_name, **kwargs).as_dict()

    def approve(self, private_endpoint_name: str, **kwargs: str):
        """
            Approve a private endpoint that is pending on the given Azure resource type
        """
        self._validate_arguments(**kwargs)
        logging.info(f"Approving private endpoint '{private_endpoint_name}'")
        existing_endpoint = self.get(private_endpoint_name, **kwargs)
        if existing_endpoint["private_link_service_connection_state"]["status"] == "Approved":
            logging.info("    Private endpoint already approved")
            return
        poller = self.management_client.private_endpoint_connections.begin_create(
            private_endpoint_name,
            **kwargs,
            request={
                "properties": {
                    "privateLinkServiceConnectionState": {
                        "description": f"Auto-Approved by {Util.get_current_user()}",
                        "status": "Approved"
                    }
                }
            }
        )
        poller.wait(300.0)
        poller.result()
        return

    def get_all(self, **kwargs: str) -> List[Dict[str, Any]]:
        """
            Return all private endpoints for the resource type class
        """
        self._validate_arguments(**kwargs)
        return [x.as_dict() for x in self.management_client.private_endpoint_connections.list(**kwargs)]

    def get_all_names(self, **kwargs: str) -> List[Dict[str, Any]]:
        """
            Return all private endpoint names for the resource type class
        """
        self._validate_arguments(**kwargs)
        return [x["name"] for x in self.get_all(**kwargs)]

    def _validate_arguments(self, **kwargs: str):
        """
            Validate the given kwargs. This should be called before interacting with the Azure client

            :raises: A ValueError if there are any missing required args, or any unexpected args
        """
        required_kwargs = self.get_required_kwargs()
        optional_kwargs = self.get_optional_kwargs()
        all_legal_kwargs = set(required_kwargs + optional_kwargs)
        missing_required_kwargs = {k for k in required_kwargs if k not in kwargs}
        if missing_required_kwargs:
            raise ValueError(f"Missing the following kwargs to {self.__class__}: {missing_required_kwargs}")
        unexpected_kwargs = {k for k in kwargs if k not in all_legal_kwargs}
        if unexpected_kwargs:
            raise ValueError(f"The following arguments were passed to {self.__class__} but were unexpected: {unexpected_kwargs}")

    @abstractmethod
    def get_client_class(cls) -> Type:
        """
            Return the Azure client that will be used to interact with private endpoints
        """
        pass

    @abstractmethod
    def get_required_kwargs(cls) -> List[str]:
        """
            Return the list of required kwarg names that are supplied to the get/approve/get_all/get_all_names functions
        """
        pass

    @abstractmethod
    def get_optional_kwargs(cls) -> List[str]:
        """
            Return the list of optional kwarg names that are supplied to the get/approve/get_all/get_all_names functions
        """
        pass
