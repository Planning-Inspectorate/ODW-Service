"""
Functions to interact with Azure Synapse
"""
from azure.identity import DefaultAzureCredential
import requests
import pprint
import os
import json

_CREDENTIAL = DefaultAzureCredential()
_API_VERSION = '2020-12-01'
_SYNAPSE_ENDPOINT = 'https://pins-synw-odw-dev-uks.dev.azuresynapse.net/notebooks/'
_NOTEBOOK = 'ci_cd_test_notebook'

_token = _CREDENTIAL.get_token("https://dev.azuresynapse.net/.default").token

_headers = {
    "Authorization": f"Bearer {_token}",
    "Content-Type": "application/json"
}

def delete_notebook(notebook: str) -> dict:
    """
    Deletes a notebook from Synapse Live Mode in the target workspace
    """
    notebook_url = f'{_SYNAPSE_ENDPOINT}{notebook}?api-version={_API_VERSION}'
    response = requests.delete(notebook_url, headers=_headers)
    return response.json()

def get_notebook(notebook: str) -> dict:
    """
    Gets a notebook from Synapse Live Mode in the target workspace
    """
    notebook_url = f'{_SYNAPSE_ENDPOINT}{notebook}?api-version={_API_VERSION}'
    response = requests.get(notebook_url, headers=_headers)
    return response.json()

def create_or_update_notebook(notebook: str) -> dict:
    """
    This currently doesn't work.
    Error: Notebook cells must be defined in the payload
    """
    notebook_url = f'{_SYNAPSE_ENDPOINT}{notebook}?api-version={_API_VERSION}'
    script_dir = os.path.dirname(__file__)
    notebook_path = os.path.join(script_dir, f"../workspace/notebook/{_NOTEBOOK}.json")
    with open(notebook_path, 'r') as file:
        notebook_data = json.load(file)

    request_body = {
        "name": _NOTEBOOK,
        "properties": notebook_data
    }

    response = requests.put(notebook_url, headers=_headers, json=request_body)
    return response.json()

def main() -> dict:
    """
    Main function
    """
    pprint.pprint(get_notebook(notebook=_NOTEBOOK))

if __name__ == '__main__':
    main()