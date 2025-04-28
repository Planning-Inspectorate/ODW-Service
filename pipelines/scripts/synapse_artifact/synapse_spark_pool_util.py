from pipelines.scripts.util import Util
from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any
import requests
import json
import time
import logging


class SynapseSparkPoolUtil(SynapseArtifactUtil):
    """
        Class for managing the retrieval and analysis of Synapse Spark Pool artifacts
    """
    @classmethod
    def get_type_name(cls) -> str:
        return "sparkPool"

    def get(self, artifact_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return self._web_request(
            f"{self.synapse_endpoint}/bigDataPools/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        response = self._web_request(
            f"{self.synapse_endpoint}/bigDataPools?api-version=2020-12-01",
        ).json()
        all_notebooks = response["value"]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_notebooks.extend(response["value"])
        return all_notebooks
    
    def create(self, pool_name: str):
        """
            Create a spark pool with default settings with the given name
        """
        synapse_workspace_id = self._web_request(f"{self.synapse_endpoint}/workspace?api-version=2020-12-01").json()["id"]
        endpoint = f"https://management.azure.com{synapse_workspace_id}/bigDataPools/{pool_name}?api-version=2021-06-01"

        payload = {
            "properties": {
                "creationDate": "0001-01-01T00:00:00",
                "sparkVersion": "3.4",
                "nodeCount": 0,
                "nodeSize": "Small",
                "nodeSizeFamily": "MemoryOptimized",
                "autoScale": {
                    "enabled": True,
                    "minNodeCount": 3,
                    "maxNodeCount": 12
                },
                "autoPause": {
                    "enabled": True,
                    "delayInMinutes": 60
                },
                "isComputeIsolationEnabled": False,
                "cacheSize": 0,
                "dynamicExecutorAllocation": {
                    "enabled": False
                },
                "isAutotuneEnabled": True,
                "provisioningState": "Succeeded"
            },
            "location": "UK South",
            "tags": dict()
        }
        access_token = json.loads(Util.run_az_cli_command(["az", "account", "get-access-token", "--output", "json"]))["accessToken"]

        resp = requests.put(
            endpoint,
            json=payload,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        max_timeout = 30
        current_timeout = 0
        provisioned = False
        # Wait for the pool to be created before continuing
        pools = self.get_all()
        wait_interval = 1
        while ((not provisioned) or pool_name not in {pool["name"] for pool in pools}) and current_timeout < max_timeout:
            logging.info(f"    Pool is being created - waiting {wait_interval} seconds before checking again...")
            time.sleep(wait_interval)
            current_timeout += wait_interval
            pools = self.get_all()
            target_pool = [x for x in pools if x["name"] == pool_name]
            if target_pool:
                logging.info(f"    The pool has been created, its provisioning state is '{target_pool[0]['properties']['provisioningState']}'")
                provisioned = target_pool[0]["properties"]["provisioningState"] == "Succeeded"
        if current_timeout >= max_timeout:
            raise RuntimeError(
                f"Exceeded max wait time when creating the spark pool '{pool_name}'. Http response was:\n {json.dumps(resp, indent=4)}"
            )

    def delete(self, pool_name: str):
        """
            Delete the spark pool with the given name
        """
        synapse_workspace_id = self._web_request(f"{self.synapse_endpoint}/workspace?api-version=2020-12-01").json()["id"]
        endpoint = f"https://management.azure.com{synapse_workspace_id}/bigDataPools/{pool_name}?api-version=2021-06-01"
        access_token = json.loads(Util.run_az_cli_command(["az", "account", "get-access-token", "--output", "json"]))["accessToken"]

        resp = requests.delete(
            endpoint,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        max_timeout = 30
        current_timeout = 0
        wait_interval = 1
        # Wait for the pool to be destroyed before continuing
        while pool_name in {pool["name"] for pool in self.get_all()} and current_timeout < max_timeout:
            logging.info(f"    Pool is being deleted - waiting {wait_interval} seconds before checking again...")
            time.sleep(wait_interval)
            current_timeout += wait_interval
        if current_timeout >= max_timeout:
            raise RuntimeError(
                f"Exceeded max wait time when deleting the spark pool '{pool_name}'. Http response was:\n {json.dumps(resp.json(), indent=4)}"
            )

    def get_uncomparable_attributes(self) -> List[str]:
        return []

    def get_nullable_attributes(self) -> List[str]:
        return []
