from azure.identity import AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential
import requests
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any, Set
import re
import json


class SynapseArtifactUtil(ABC):
    def __init__(self, workspace_name: str):
        self.workspace_name = workspace_name
        credential = ChainedTokenCredential(
            #ManagedIdentityCredential(),
            AzureCliCredential()
        )
        self._token = credential.get_token("https://dev.azuresynapse.net").token
        self.synapse_endpoint = f"https://{self.workspace_name}.dev.azuresynapse.net"

    def _web_request(self, endpoint: str) -> requests.Response:
        """
            Submit a http request against the specified endpoint
        """
        api_call_headers = {'Authorization': 'Bearer ' + self._token}
        return requests.get(endpoint, headers=api_call_headers)

    @abstractmethod
    def get(self, artifact_name: str) -> Dict[str, Any]:
        """
            Return the properties for the given artifact
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """
            Return all artifacts
        """
        pass

    @abstractmethod
    def compare(self, artifact_a: Dict[str, Any], artifact_b: Dict[str, Any]) -> bool:
        """
            Compare two artifacts. Return true if they match, false otherwise
        """
        pass

    def is_property_empty(self, property: Union[Dict[str, Any], List[Any], Any]) -> bool:
        """
            Return if the given property is empty, return false otherwise.
            A property is considered empty if it is null, empty or all of its children are empty
        """
        if isinstance(property, dict):
            if not property:
                return True
            for key, value in property.items():
                if not self.is_property_empty(value):
                    return False
            return True
        if isinstance(property, list):
            if not property:
                return True
            for elem in property:
                if elem:
                    return False
            return True
        return property is None

    def get_all_properties(self, target_json: Dict[str, Any]) -> Set[str]:
        """
            Return all properties from the given json

            e.g
            ```
            my_json = {
                "some": 1,
                "properties": 2,
                "list_type": [
                    "a"
                ],
                "dict_type": {
                    "b": 3,
                    "c": 4
                }
            }
            ```
            get_all_properties(my_json)

            Will return

            {
                "some",
                "properties",
                "list_type",
                "list_type.0",
                "dict_type",
                "dict_type.b",
                "dict_type.c"
            }
        """
        set(self._extract_dict_keys(target_json, current_level="").keys())

    def _extract_list_keys(self, target_list: List[Any], current_level: str) -> Dict[str, None]:
        """
            Extract property names from the given list

            e.g.
            ```
            my_list = ["a", {"list": 1, "of": 2, "properties": 3}]
            _extract_list_keys(my_list, "some_prefix")
            >> {
                "some_prefix": None
                "some_prefix.0": None,
                "some_prefix.1": None,
                "some_prefix.1.list": None,
                "some_prefix.1.of": None,
                "some_prefix.1.properties": None
            }
            ```
        """
        current_level_prefix = f"{current_level}." if current_level else ""
        dict_keys = {current_level: None}
        for i, val in enumerate(target_list):
            new_level = f"{current_level_prefix}{i}"
            if isinstance(val, dict):
                dict_keys = dict(dict_keys, **self._extract_dict_keys(val, new_level))
            elif isinstance(val, list):
                dict_keys = dict(dict_keys, **self._extract_list_keys(val, new_level))
            else:
                dict_keys[new_level] = None
        return dict_keys

    def _extract_dict_keys(self, target_dict: Dict[str, Any], current_level: str = "") -> Dict[str, None]:
        """
            Extract property names from the given dictionary

            e.g.
            ```
            my_dict = {"group": 1, "of": 2, "properties": 3, "a_list": {"a", "b", "c}, "nested": {"a": 1, "b"; 2}}
            _extract_list_keys(my_dict, "some_prefix")
            >> {
                "some_prefix": None,
                "some_prefix.group": None,
                "some_prefix.of": None,
                "some_prefix.properties": None,
                "some_prefix.a_list": None,
                "some_prefix.a_list.0": None,
                "some_prefix.a_list.1": None,
                "some_prefix.a_list.2": None,
                "some_prefix.nested": None,
                "some_prefix.nested.a": None,
                "some_prefix.nested.b": None
            }
            ```
        """
        current_level_prefix = f"{current_level}." if current_level else ""
        dict_keys = {current_level: None} if current_level else dict()
        dict_keys = dict(
            dict_keys,
            **{
                f"{current_level_prefix}{key}": None
                for key in target_dict.keys()
            }
        )
        for key, val in target_dict.items():
            new_level = f"{current_level_prefix}{key}"
            if isinstance(val, dict):
                dict_keys[new_level] = None
                dict_keys = dict(dict_keys, **self._extract_dict_keys(val, new_level))
            elif isinstance(val, list):
                dict_keys = dict(dict_keys, **self._extract_list_keys(val, new_level))
            else:
                dict_keys[new_level] = None
        return dict_keys
    
    def clean_json_properties(
            self,
            json_dict: Dict[str, Any],
            properties: Set[str],
            uncomparable_properties: Set[str],
            nullable_properties: Set[str]
        ) -> Set[str]:
        """
            Remove uncomparable properties, or nullified properties from the given json
        """
        def extract_value_from_property(json_dict: Dict[str, Any], property: str) -> Any:
            """
                Access json properties by a dot-notation string.
                e.g `extract_value_from_property({"a": {"b": 2}}, "a.b") -> 2`
            """
            property_split = property.split(".")
            property_value = json_dict
            for subproperty in property_split:
                if isinstance(property_value, dict):
                    property_value = property_value[subproperty]
                elif isinstance(property_value, list):
                    property_value = property_value[int(subproperty)]
                else:
                    raise ValueError(f"Could not access property {property_value} by key '{subproperty}'")
            return property_value

        return [
            property
            for property in properties
            if (
                (not any(re.match(pattern, property) for pattern in uncomparable_properties)) and
                (
                    (not any(re.match(pattern, property) for pattern in nullable_properties)) or
                    (
                        any(re.match(pattern, property) for pattern in nullable_properties) and
                        not self.is_property_empty(extract_value_from_property(json_dict, property))
                    )
                )
            )
        ]
    
