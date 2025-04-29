from azure.identity import AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential
import requests
from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any, Set
import re
import logging
import json
import os

logging.basicConfig(level=logging.INFO)


class SynapseArtifactUtil(ABC):
    """
        Abstract class for managing the retrieval and analysis of Synapse artifacts
    """
    credential = ChainedTokenCredential(
        #ManagedIdentityCredential(),
        AzureCliCredential()
    )
    _token = credential.get_token("https://dev.azuresynapse.net").token
    def __init__(self, workspace_name: str):
        """
            :param workspace_name: The name of the Synapse workspace
        """
        self.workspace_name = workspace_name
        self.synapse_endpoint = f"https://{self.workspace_name}.dev.azuresynapse.net"
    
    @classmethod
    @abstractmethod
    def get_type_name(cls) -> str:
        pass

    def _web_request(self, endpoint: str) -> requests.Response:
        """
            Submit a http request against the specified endpoint

            :param endpooint: The url to send the request to
            :return: The http response
        """
        api_call_headers = {'Authorization': 'Bearer ' + self._token}
        return requests.get(endpoint, headers=api_call_headers)

    @abstractmethod
    def get(self, artifact_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
            Return the attributes for the given artifact

            :param artifact_name: The name of the artifact to fetch from the Synapse REST API
            :param kwargs: Any additional arguments that are required
            :return: The json object retrieved by the Synapse REST API
        """
        pass

    @abstractmethod
    def get_all(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
            Return all artifacts

            :param kwargs: Any additional arguments that are required
            :return: A list of json objects retrieved by the Synapse REST API
        """
        pass

    def download_live_workspace(self, local_folder: str):
        """
            Download all artifacts to a local folder
            
            :param local_folder: Where to store
        """
        artifacts = self.get_all()
        logging.info(f"Downloaded {len(artifacts)} artifacts of type '{self.get_type_name()}'")
        base_folder = f"{local_folder}/{self.get_type_name()}"
        os.makedirs(base_folder)
        for artifact in artifacts:
            artifact_name = artifact["name"]
            with open(f"{base_folder}/{artifact_name}.json", "w") as f:
                json.dump(artifact, f, indent=4)

    @abstractmethod
    def get_uncomparable_attributes(self) -> List[str]:
        """
            :return: Regex patterns of attributes that should not be compared for this kind of artifact
        """
        pass

    @abstractmethod
    def get_nullable_attributes(self) -> List[str]:
        """
            :return: Regex patterns of attributes that should be dropped if null for this kind of artifact
        """
        pass

    def compare(self, artifact_a: Dict[str, Any], artifact_b: Dict[str, Any]) -> bool:
        """
            Compare two artifacts.

            :param artifact_a: The json for the first artifact to compare
            :param artifact_b: The json for the second artifact to compare
            :return: True if the artifacts match, False otherwise
        """
        uncomparable_attributes = self.get_uncomparable_attributes()
        nullable_attributes = self.get_nullable_attributes()
        artifact_a_attributes = self._extract_dict_attributes(artifact_a)
        artifact_b_attributes = self._extract_dict_attributes(artifact_b)
        artifact_a_attributes_cleaned = self.clean_attributes(
            artifact_a_attributes,
            artifact_a,
            uncomparable_attributes,
            nullable_attributes
        )
        artifact_b_attributes_cleaned = self.clean_attributes(
            artifact_b_attributes,
            artifact_b,
            uncomparable_attributes,
            nullable_attributes
        )
        if artifact_a_attributes_cleaned != artifact_b_attributes_cleaned:
            return False
        return self._compare_dictionaries_by_attributes(artifact_a_attributes_cleaned, artifact_a, artifact_b)

    def is_attribute_value_empty(self, attribute_value: Union[Dict[str, Any], List[Any], Any]) -> bool:
        """
            Return if the given attribute_value is empty, return false otherwise.

            :param attribute_value: The attribute_value to check
            :return: True if the bool(attribute_value) evaluates to False or if all of its children are empty. False otherwise
        """
        if isinstance(attribute_value, dict):
            if not attribute_value:
                return True
            for value in attribute_value.values():
                if not self.is_attribute_value_empty(value):
                    return False
            return True
        if isinstance(attribute_value, list):
            if not attribute_value:
                return True
            for elem in attribute_value:
                if elem:
                    return False
            return True
        return not bool(attribute_value)

    def get_all_attributes(self, artifact_json: Dict[str, Any]) -> Set[str]:
        """
            Return all attributes from the given json in dot notation

            :param artifact_json: The json object to get attributes for
            :return: The attributes of the json object, in dot-notation. e.g: some.attribute.of.the.json.object

            e.g
            ```
            my_json = {
                "some": 1,
                "attributes": 2,
                "list_type": [
                    "a"
                ],
                "dict_type": {
                    "b": 3,
                    "c": 4
                }
            }
            # Then
            get_all_attributes(my_json)
            # Will return
            {
                "some",
                "attributes",
                "list_type.0",
                "dict_type.b",
                "dict_type.c"
            }
            ```
        """
        set(self._extract_dict_attributes(artifact_json, current_level="").keys())

    def _extract_list_attributes(self, target_list: List[Any], current_level: str) -> Dict[str, None]:
        """
            Extract attribute names from the given list in dot-notation

            :param target_list: The list to extract attributes from
            :param current_level: String used to prefix any new attributes with. Used to identify the depth of the analysis so far
            :return: Extracted attributes as a dict of the form <attribute: None>. (A dict is used to preserve the order of the attributes)

            e.g.
            ```
            my_list = ["a", {"list": 1, "of": 2, "attributes": 3}]
            _extract_list_attributes(my_list, "some_prefix")
            # Returns
            {
                "some_prefix.0": None,
                "some_prefix.1.list": None,
                "some_prefix.1.of": None,
                "some_prefix.1.attributes": None
            }
            ```
        """
        current_level_prefix = f"{current_level}." if current_level else ""
        dict_keys = dict()
        for i, val in enumerate(target_list):
            new_level = f"{current_level_prefix}{i}"
            if isinstance(val, dict):
                dict_keys = dict(dict_keys, **self._extract_dict_attributes(val, new_level))
            elif isinstance(val, list):
                dict_keys = dict(dict_keys, **self._extract_list_attributes(val, new_level))
            else:
                dict_keys[new_level] = None
        return dict_keys

    def _extract_dict_attributes(self, target_dict: Dict[str, Any], current_level: str = "") -> Dict[str, None]:
        """
            Extract attribute names from the given dictionary

            :param target_dict: The dictionary to extract attributes from
            :param current_level: String used to prefix any new attributes with. Used to identify the depth of the analysis so far
            :return: Extracted attributes as a dict of the form <attribute: None>. (A dict is used to preserve the order of the attributes)

            e.g.
            ```
            my_dict = {"group": 1, "of": 2, "attributes": 3, "a_list": {"a", "b", "c}, "nested": {"a": 1, "b"; 2}}
            _extract_list_attributes(my_dict, "some_prefix")
            # Returns
            {
                "some_prefix": None,
                "some_prefix.group": None,
                "some_prefix.of": None,
                "some_prefix.attributes": None,
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
                dict_keys = dict(dict_keys, **self._extract_dict_attributes(val, new_level))
            elif isinstance(val, list):
                dict_keys = dict(dict_keys, **self._extract_list_attributes(val, new_level))
            else:
                dict_keys[new_level] = None
        return dict_keys
    
    def clean_attributes(
        self,
        attributes: Set[str],
        artifact_json: Dict[str, Any],
        uncomparable_attributes: Set[str],
        nullable_attributes: Set[str]
    ) -> Set[str]:
        """
            Return the attributes that can be compared, and are nullable but with non-null values

            :param artifact_json: The artifact the attributes belong to
            :param attributes: The attributes to clean, in dot-notation
            :param uncomparable_attributes: The attributes that should be ignored and removed from the output
            :param nullable_attributes: The attributes that should be removed only if their value is null in the artifact_json
            :return: All attributes with concrete values that can be compared against another attribute set
        """
        return {
            attribute
            for attribute in attributes
            if (
                (not any(re.match(pattern, attribute) for pattern in uncomparable_attributes)) and
                (
                    (not any(re.match(pattern, attribute) for pattern in nullable_attributes)) or
                    (
                        any(re.match(pattern, attribute) for pattern in nullable_attributes) and
                        not self.is_attribute_value_empty(self._extract_dictionary_value_by_attribute(artifact_json, attribute))
                    )
                )
            )
        }

    def _extract_dictionary_value_by_attribute(self, dictionary: Dict[str, Any], attribute: str) -> Any:
        """
            Access json attributes by a dot-notation string.
            e.g `extract_value_from_attribute({"a": {"b": 2}}, "a.b") -> 2`

            :param dictionary: The json artifact to extract the attribute from
            :param attribute: The attribute to extract, in dot-notation
            :return: The attribute value
            :raises: An exception is raised if the given inputs are invalid
        """
        attribute_split = attribute.split(".")
        attribute_value = dictionary
        for i, subattribute in enumerate(attribute_split):
            remaining_subattributes = ".".join(attribute_split[i:])
            if remaining_subattributes in attribute_value:
                # This is for cases like spark variables which may be stored in the json
                return attribute_value[remaining_subattributes]
            if isinstance(attribute_value, dict):
                if subattribute not in attribute_value:
                    raise ValueError(f"Unable to extract subattribute '{subattribute}' from {attribute_value}. Full attribute name is '{attribute}'")
                attribute_value = attribute_value[subattribute]
            elif isinstance(attribute_value, list):
                if int(subattribute) >= len(attribute_value):
                    raise ValueError(f"Unable to extract subattribute '{subattribute}' from {attribute_value}. Full attribute name is '{attribute}'")
                attribute_value = attribute_value[int(subattribute)]
            else:
                if i != len(attribute_split) - 1:
                    # Only allow returning leaf values if they are the last name to be resolved
                    raise ValueError(f"Could not access attribute {attribute_value} by key '{subattribute}' - the value is not a collection")
        return attribute_value

    def _compare_dictionaries_by_attributes(self, attributes: Set[str], dict_a: Dict[str, Any], dict_b: Dict[str, Any]) -> Dict[str, bool]:
        """
            Compare each attribute between the two dictionaries

            :param attributes: The attributes to compare, in dot-notation
            :param dict_a: First dictionary to compare
            :param dict_b: Second dictionary to compare
            :return: True if the dictionaries match, False otherwise.
        """
        for attribute in attributes:
            val_a = self._extract_dictionary_value_by_attribute(dict_a, attribute)
            val_b = self._extract_dictionary_value_by_attribute(dict_b, attribute)
            if val_a != val_b:
                logging.info(
                    (
                        f"Mismatch between artifacts for attribute '{attribute}'. {json.dumps(val_a, indent=4)} != {json.dumps(val_b, indent=4)}"
                        ". Ending comparison of artifacts"
                    )
                )
                return False
        return True
