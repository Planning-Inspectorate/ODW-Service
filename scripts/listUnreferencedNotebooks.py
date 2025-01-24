#pip install azure-mgmt-synapse azure-identity requests

import requests
from azure.identity import DefaultAzureCredential

# Replace these with your actual values
subscription_id = 'ff442a29-fc06-4a13-8e3e-65fd5da513b3'
resource_group_name = 'pins-rg-data-odw-dev-uks'
workspace_name = 'pins-synw-odw-dev-uks'

# Use DefaultAzureCredential to authenticate
credential = DefaultAzureCredential()

# Get an access token for the REST API
token = credential.get_token('https://dev.azuresynapse.net/.default').token

# Define the base URL for Synapse Workspace REST API
base_url = "https://pins-synw-odw-dev-uks.dev.azuresynapse.net/"

# Function to get a list of notebooks
def get_notebooks():
    notebooks_url = f'{base_url}notebooks?api-version=2020-12-01'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(notebooks_url, headers=headers)
    
    if response.status_code == 200:
        notebooks = response.json()['value']
        return [notebook['name'] for notebook in notebooks]
    else:
        raise Exception(f"Error retrieving notebooks: {response.text}")

# Function to get all pipeline names and their notebook references
def get_pipeline_references():
    pipeline_references = set()
    pipelines_url = f'{base_url}pipelines?api-version=2020-12-01'
    print(pipelines_url)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(pipelines_url, headers=headers)
    
    print(response.status_code)

    if response.status_code == 200:

        print(response.json())

        pipelines = response.json()['value']
        for pipeline in pipelines:
            pipeline_name = pipeline['name']
            print(f"Checking {pipeline_name}")
            pipeline_definition_url = f'{base_url}pipelines/{pipeline_name}?api-version=2021-06-01'
            pipeline_def_response = requests.get(pipeline_definition_url, headers=headers)
            
            if pipeline_def_response.status_code == 200:
                pipeline_definition = pipeline_def_response.json()
                # Check for ExecuteNotebook activities
                activities = pipeline_definition.get('properties', {}).get('activities', [])
                for activity in activities:
                    if activity['type'] == 'SynapseNotebook':
                        try:
                            notebook_name = activity['typeProperties']['notebook']['referenceName']
                            print(f"\t\t{notebook_name}")
                            pipeline_references.add(notebook_name)
                        except:
                            print("invalid data")
            else:
                print("FAILED TO READ PIPELINES")
    else:
        print(f"{response.text}")
        raise Exception(f"Error retrieving pipelines: {response.text}")
    
    return pipeline_references

# Main logic to find unreferenced notebooks
def find_unreferenced_notebooks():
    referenced_notebooks = get_pipeline_references()

    list_referenced_notebooks = list(set(referenced_notebooks))
    print("*********** REFERENCED NOTEBOOKS ***********")
    for notebook in list_referenced_notebooks:
        print(notebook)
    print("********************************************")

    notebooks = get_notebooks()
    
    # Find notebooks that are not referenced by any pipeline
    unreferenced_notebooks = set(notebooks) - referenced_notebooks
    return unreferenced_notebooks

# Get unreferenced notebooks
unreferenced_notebooks = find_unreferenced_notebooks()

# Print out the unreferenced notebooks
print('########################################')
print("Notebooks not referenced by pipelines:")
print('########################################')
for notebook in unreferenced_notebooks:
    print(notebook)
print('########################################')
