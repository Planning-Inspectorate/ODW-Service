from azure.identity import AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential
import requests
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any, Set
import re
import logging
import json

logging.basicConfig(level=logging.INFO)


class SynapseArtifactUtil(ABC):
    def __init__(self, workspace_name: str):
        """
            :param workspace_name: The name of the Synapse workspace
        """
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

            :param endpooint: The url to send the request to
            :return: The http response
        """
        api_call_headers = {'Authorization': 'Bearer ' + self._token}
        return requests.get(endpoint, headers=api_call_headers)

    @abstractmethod
    def get(self, artifact_name: str) -> Dict[str, Any]:
        """
            Return the properties for the given artifact

            :param artifact_name: The name of the artifact to fetch from the Synapse REST API
            :return: The json object retrieved by the Synapse REST API
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """
            Return all artifacts

            :return: A list of json objects retrieved by the Synapse REST API
        """
        pass

    @abstractmethod
    def get_uncomparable_properties(self) -> List[str]:
        """
            :return: Regex patterns of properties that should not be compared for this kind of artifact
        """
        pass

    @abstractmethod
    def get_nullable_properties(self) -> List[str]:
        """
            :return: Regex patterns of properties that should be dropped if null for this kind of artifact
        """
        pass

    def compare(self, artifact_a: Dict[str, Any], artifact_b: Dict[str, Any]) -> bool:
        """
            Compare two artifacts.

            :param artifact_a: The json for the first artifact to compare
            :param artifact_b: The json for the second artifact to compare
            :return: True if the artifacts match, False otherwise
        """
        uncomparable_properties = self.get_uncomparable_properties()
        nullable_properties = self.get_nullable_properties()
        artifact_a_properties = self._extract_dict_properties(artifact_a)
        artifact_b_properties = self._extract_dict_properties(artifact_b)
        artifact_a_properties_cleaned = self.clean_json_properties(
            artifact_a,
            artifact_a_properties,
            uncomparable_properties,
            nullable_properties
        )
        artifact_b_properties_cleaned = self.clean_json_properties(
            artifact_b,
            artifact_b_properties,
            uncomparable_properties,
            nullable_properties
        )
        if artifact_a_properties_cleaned != artifact_b_properties_cleaned:
            return False
        return self._compare_properties(artifact_a_properties_cleaned, artifact_a, artifact_b)

    def is_property_empty(self, property: Union[Dict[str, Any], List[Any], Any]) -> bool:
        """
            Return if the given property is empty, return false otherwise.

            :param property: The property to check
            :return: True if the bool(property) evaluates to False or if all of its children are empty. False otherwise
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
        return not bool(property)

    def get_all_properties(self, target_json: Dict[str, Any]) -> Set[str]:
        """
            Return all properties from the given json in dot notation

            :param target_json: The json object to get properties for
            :return: The properties of the json object, in dot-notation. e.g: some.property.of.the.json.object

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
            # Then
            get_all_properties(my_json)
            # Will return
            {
                "some",
                "properties",
                "list_type.0",
                "dict_type.b",
                "dict_type.c"
            }
            ```
        """
        set(self._extract_dict_properties(target_json, current_level="").keys())

    def _extract_list_properties(self, target_list: List[Any], current_level: str) -> Dict[str, None]:
        """
            Extract property names from the given list in dot-notation

            :param target_list: The list to extract properties from
            :param current_level: String used to prefix any new properties with. Used to identify the depth of the analysis so far
            :return: Extracted properties as a dict of the form <property: None>. (A dict is used to preserve the order of the properties)

            e.g.
            ```
            my_list = ["a", {"list": 1, "of": 2, "properties": 3}]
            _extract_list_properties(my_list, "some_prefix")
            # Returns
            {
                "some_prefix.0": None,
                "some_prefix.1.list": None,
                "some_prefix.1.of": None,
                "some_prefix.1.properties": None
            }
            ```
        """
        current_level_prefix = f"{current_level}." if current_level else ""
        dict_keys = dict()
        for i, val in enumerate(target_list):
            new_level = f"{current_level_prefix}{i}"
            if isinstance(val, dict):
                dict_keys = dict(dict_keys, **self._extract_dict_properties(val, new_level))
            elif isinstance(val, list):
                dict_keys = dict(dict_keys, **self._extract_list_properties(val, new_level))
            else:
                dict_keys[new_level] = None
        return dict_keys

    def _extract_dict_properties(self, target_dict: Dict[str, Any], current_level: str = "") -> Dict[str, None]:
        """
            Extract property names from the given dictionary

            :param target_dict: The dictionary to extract properties from
            :param current_level: String used to prefix any new properties with. Used to identify the depth of the analysis so far
            :return: Extracted properties as a dict of the form <property: None>. (A dict is used to preserve the order of the properties)

            e.g.
            ```
            my_dict = {"group": 1, "of": 2, "properties": 3, "a_list": {"a", "b", "c}, "nested": {"a": 1, "b"; 2}}
            _extract_list_properties(my_dict, "some_prefix")
            # Returns
            {
                "some_prefix": None,
                "some_prefix.group": None,
                "some_prefix.of": None,
                "some_prefix.properties": None,
                "some_prefix.a_list.0": None,
                "some_prefix.a_list.1": None,
                "some_prefix.a_list.2": None,
                "some_prefix.nested.a": None,
                "some_prefix.nested.b": None
            }
            ```
        """
        current_level_prefix = f"{current_level}." if current_level else ""
        dict_keys = dict()
        for key, val in target_dict.items():
            new_level = f"{current_level_prefix}{key}"
            if isinstance(val, dict):
                dict_keys = dict(dict_keys, **self._extract_dict_properties(val, new_level))
            elif isinstance(val, list):
                dict_keys = dict(dict_keys, **self._extract_list_properties(val, new_level))
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
            Return the properties that can be compared, and are nullable but with non-null values

            :param json_dict: The artifact the properties belong to
            :param properties: The properties to clean, in dot-notation
            :param uncomparable_properties: The properties that should be ignored and removed from the output
            :param nullable_properties: The properties that should be removed only if their value is null in the json_dict
            :return: All properties with concrete values that can be compared against another property set
        """
        return {
            property
            for property in properties
            if (
                (not any(re.match(pattern, property) for pattern in uncomparable_properties)) and
                (
                    (not any(re.match(pattern, property) for pattern in nullable_properties)) or
                    (
                        any(re.match(pattern, property) for pattern in nullable_properties) and
                        not self.is_property_empty(self._extract_value_from_property(json_dict, property))
                    )
                )
            )
        }
    
    def _extract_value_from_property(self, artifact_json: Dict[str, Any], property: str) -> Any:
        """
            Access json properties by a dot-notation string.
            e.g `extract_value_from_property({"a": {"b": 2}}, "a.b") -> 2`

            :param artifact_json: The json artifact to extract the property from
            :param property: The property to extract, in dot-notation
            :return: The property value
            :raises: An exception is raised if the given inputs are invalid
        """
        property_split = property.split(".")
        property_value = artifact_json
        for i, subproperty in enumerate(property_split):
            remaining_subproperties = ".".join(property_split[i:])
            if remaining_subproperties in property_value:
                # This is for cases like spark variables which may be stored in the json
                return property_value[remaining_subproperties]
            if isinstance(property_value, dict):
                if subproperty not in property_value:
                    raise ValueError(f"Unable to extract subproperty '{subproperty}' from {property_value}. Full property name is '{property}'")
                property_value = property_value[subproperty]
            elif isinstance(property_value, list):
                if int(subproperty) >= len(property_value):
                    raise ValueError(f"Unable to extract subproperty '{subproperty}' from {property_value}. Full property name is '{property}'")
                property_value = property_value[int(subproperty)]
            else:
                if i != len(property_split) - 1:
                    # Only allow returning leaf values if they are the last name to be resolved
                    raise ValueError(f"Could not access property {property_value} by key '{subproperty}' - the value is not a collection")
        return property_value

    def _compare_properties(self, properties: Set[str], dict_a: Dict[str, Any], dict_b: Dict[str, Any]) -> Dict[str, bool]:
        """
            Compare each property between the two dictionaries

            :param properties: The properties to compare, in dot-notation
            :param dict_a: First dictionary to compare
            :param dict_b: Second dictionary to compare
            :return: True if the dictionaries match, False otherwise.
        """
        for property in properties:
            val_a = self._extract_value_from_property(dict_a, property)
            val_b = self._extract_value_from_property(dict_b, property)
            if val_a != val_b:
                logging.info(
                    (
                        f"Mismatch between artifacts for property '{property}'. {json.dumps(val_a, indent=4)} != {json.dumps(val_b, indent=4)}"
                        ". Ending comparison of artifacts"
                    )
                )
                return False
        return True
