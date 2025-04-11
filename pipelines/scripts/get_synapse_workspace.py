from azure.identity import AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential
from typing import List, Dict, Any, Callable
import requests
import json
import os
import shutil
import logging


logging.basicConfig(level=logging.INFO)


class SynapseWorkspaceUtil:
    def __init__(self, workspace_name: str):
        self.workspace_name = workspace_name
    
    def _web_request(self, endpoint: str):
        credential = ChainedTokenCredential(
            #ManagedIdentityCredential(),
            AzureCliCredential()
        )
        token = credential.get_token("https://dev.azuresynapse.net").token
        api_call_headers = {'Authorization': 'Bearer ' + token}
        return requests.get(endpoint, headers=api_call_headers)

    def get_notebook(self, notebook_name: str) -> Dict[str, Any]:
        return self._web_request(
            f"https://{self.workspace_name}.dev.azuresynapse.net/notebooks/{notebook_name}?api-version=2020-12-01",
        ).json()

    def get_all_notebooks(self) -> List[Dict[str, Any]]:
        response = self._web_request(
            f"https://{self.workspace_name}.dev.azuresynapse.net/notebooks?api-version=2020-12-01",
        ).json()
        all_notebooks = [response["value"]]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_notebooks.extend(response["value"])
        return all_notebooks

    def get_pipeline(self, pipeline_name: str) -> Dict[str, Any]:
        return self._web_request(
            f"https://{self.workspace_name}.dev.azuresynapse.net/pipelines/{pipeline_name}?api-version=2020-12-01",
        ).json()

    def get_all_pipelines(self) -> List[Dict[str, Any]]:
        return self._web_request(
            f"https://{self.workspace_name}.dev.azuresynapse.net/pipelines?api-version=2020-12-01",
        ).json()["value"]

    def get_trigger(self, trigger_name: str):
        return self._web_request(
            f"https://{self.workspace_name}.dev.azuresynapse.net/triggers/{trigger_name}?api-version=2020-12-01",
        ).json()

    def get_all_triggers(self) -> List[Dict[str, Any]]:
        return self._web_request(
            f"https://{self.workspace_name}.dev.azuresynapse.net/triggers?api-version=2020-12-01",
        ).json()["value"]

    def _download_all(self, local_folder: str, subfolder: str, get_all_function: Callable):
        base_folder = f"{local_folder}/{subfolder}"
        os.makedirs(base_folder)
        all_artifacts = get_all_function()
        logging.info(f"Download {len(all_artifacts)} artifacts of type '{subfolder}'")
        for artifact in all_artifacts:
            artifact_name = artifact["name"]
            with open(f"{base_folder}/{artifact_name}.json", "w") as f:
                json.dump(artifact, f, indent=4)

    def _download_all_notebooks(self, local_folder: str):
        self._download_all(local_folder, "notebook", self.get_all_notebooks)

    def _download_all_pipelines(self, local_folder: str):
        self._download_all(local_folder, "pipeline", self.get_all_pipelines)

    def _download_all_triggers(self, local_folder: str):
        self._download_all(local_folder, "trigger", self.get_all_triggers)

    def download_workspace(self, local_folder: str):
        if os.path.exists(local_folder):
            shutil.rmtree(local_folder)
        os.makedirs(local_folder)
        self._download_all_notebooks(local_folder)
        self._download_all_pipelines(local_folder)
        self._download_all_triggers(local_folder)


if __name__ == "__main__":
    #SynapseWorkspaceUtil("pins-synw-odw-dev-uks").download_workspace("my_local_workspace")

    all_nb = SynapseWorkspaceUtil("pins-synw-odw-dev-uks").get_all_notebooks()
    print("count: ", len(all_nb))
   # print(json.dumps(all_nb, indent=4))
