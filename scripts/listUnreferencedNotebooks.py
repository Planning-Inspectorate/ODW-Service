#pip install azure-mgmt-synapse azure-identity requests

import requests
import os
import re

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


#get a list of all of the pipelines (paginated)
def read_paginated_data(url, headers):
    data = []
    while url:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        data.extend(response_json.get('value', []))
        url = response_json.get('nextLink')
    return data


# Function to get a list of notebooks
def get_notebooks():
    notebooks_url = f'{base_url}notebooks?api-version=2020-12-01'
    print(f"Reading from {notebooks_url}")
    headers = {'Authorization': f'Bearer {token}'}
    notebooks = read_paginated_data(notebooks_url, headers=headers)
    
    if notebooks:
        return [notebook['name'] for notebook in notebooks]
    else:
        raise Exception(f"Error retrieving notebooks")

# Function to get all pipeline names and their notebook references
def get_pipeline_references():
    pipeline_references = set()
    pipelines_url = f'{base_url}pipelines?api-version=2020-12-01'
    headers = {'Authorization': f'Bearer {token}'}
    pipelines = read_paginated_data(pipelines_url, headers=headers)
    
    if pipelines:
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


        print('**************** LIST OF PIPELINES *******************')
        for pipeline in pipelines:
            print(pipeline['name'])
        print('**************** END OF LIST OF PIPELINES *******************')            
    else:
        raise Exception(f"Error retrieving pipelines")
    
    return pipeline_references

# Main logic to find unreferenced notebooks
def find_unreferenced_notebooks():
    referenced_notebooks = get_pipeline_references()

    list_referenced_notebooks = list(set(referenced_notebooks))
    print("*********** LIST OF REFERENCED NOTEBOOKS ***********")
    for notebook in list_referenced_notebooks:
        print(notebook)
    print("*********** END OF LIST OF REFERENCED NOTEBOOKS ***********")

    notebooks = get_notebooks()
    
    # Find notebooks that are not referenced by any pipeline
    unreferenced_notebooks = set(notebooks) - referenced_notebooks
    return unreferenced_notebooks


def grep_files(pattern, root_dir):
    # Compile the regular expression pattern
    regex = re.compile(pattern)
    notebooks = set()
    
    # Walk through the directory
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        match = regex.search(line)
                        if (match is not None):
                            notebooks.add(f"{match.group(1).strip()}")
            except (UnicodeDecodeError, FileNotFoundError):
                # Skip files that can't be read
                continue
    return notebooks

# Example usage
pattern = r'\"%run.+\/(.+).*\"'
root_dir = '../workspace/notebook/'
source_notebooks = grep_files(pattern, root_dir)

for source_notebook in source_notebooks:
    print(source_notebook)

# Get unreferenced notebooks
#unreferenced_notebooks = find_unreferenced_notebooks()

# Print out the unreferenced notebooks
#print("*********** LIST OF UNREFERENCED NOTEBOOKS ***********")
#for notebook in unreferenced_notebooks:
#    print(notebook)
#print("*********** END OF LIST OF UNREFERENCED NOTEBOOKS ***********")
