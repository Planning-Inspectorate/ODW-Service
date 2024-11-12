from azure.identity import DefaultAzureCredential
import requests
import pprint
import os
import json

CREDENTIAL = DefaultAzureCredential()
API_VERSION = '2020-12-01'
SYNAPSE_ENDPOINT = 'https://pins-synw-odw-dev-uks.dev.azuresynapse.net/notebooks/'
NOTEBOOK = 'ci_cd_test_notebook'

token = CREDENTIAL.get_token("https://dev.azuresynapse.net/.default").token

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

def delete_notebook(notebook: str) -> dict:
    """
    Deletes a notebook from Synapse Live Mode in the target workspace
    """
    notebook_url = f'{SYNAPSE_ENDPOINT}{notebook}?api-version={API_VERSION}'
    response = requests.delete(notebook_url, headers=headers)
    data = response.json()
    return data

def get_notebook(notebook: str) -> dict:
    """
    Gets a notebook from Synapse Live Mode in the target workspace
    """
    notebook_url = f'{SYNAPSE_ENDPOINT}{notebook}?api-version={API_VERSION}'
    response = requests.get(notebook_url, headers=headers)
    data = response.json()
    return data

def create_or_update_notebook(notebook: str) -> dict:

    
    """
    This currently doesn't work.
    Error: Notebook cells must be defined in the payload
    """
    notebook_url = f'{SYNAPSE_ENDPOINT}{notebook}?api-version={API_VERSION}'
    script_dir = os.path.dirname(__file__)
    notebook_path = os.path.join(script_dir, f"../workspace/notebook/{NOTEBOOK}.json")
    with open(notebook_path, 'r') as file:
        notebook_data = json.load(file)

    request_body = {
        "name": NOTEBOOK,
        "properties": notebook_data
    }

    response = requests.put(notebook_url, headers=headers, json=request_body)
    data = response.json()
    return data

def main():
    pprint.pprint(get_notebook(notebook=NOTEBOOK))

if __name__ == '__main__':
    main()