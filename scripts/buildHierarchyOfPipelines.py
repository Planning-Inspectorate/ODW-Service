import requests
import os
import re
import json
import jsonpath_rw_ext
from jsonpath_ng.ext import parse
from anytree import Node, RenderTree, AsciiStyle, findall,PreOrderIter

from azure.identity import DefaultAzureCredential

import sys
sys.stdout = open('hierarchy.txt','wt')

# Replace these with your actual values
environment = "dev"
subscription_id = 'ff442a29-fc06-4a13-8e3e-65fd5da513b3'
resource_group_name = f'pins-rg-data-odw-{environment}-uks'
workspace_name = f'pins-synw-odw-{environment}-uks'

# Use DefaultAzureCredential to authenticate
credential = DefaultAzureCredential()

# Get an access token for the REST API
token = credential.get_token(f'https://dev.azuresynapse.net/.default').token

# Define the base URL for Synapse Workspace REST API
base_url = f"https://pins-synw-odw-{environment}-uks.dev.azuresynapse.net/"

#get a list of all of the pipelines (paginated)
def read_paginated_data(url, headers):
    data = []
    while url:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        data.extend(response_json.get('value', []))
        url = response_json.get('nextLink')
    return data

def read_paginated_data_post(url, data, headers):
    response_data = []
    continuationToken = ''
    while continuationToken is not None:
        #print(f"Reading from {url}")
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()
        response_data.extend(response_json.get('value', []))
        
        tokenData = response_json.get('continuationToken')
        if tokenData is not None:
            continuationToken = tokenData
            data['continuationToken'] = tokenData
        
        if tokenData is None:
            continuationToken = None
            break
        
    return response_data

def get_pipeline_runs():
    runs_url = f'{base_url}queryPipelineRuns?api-version=2020-12-01'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "lastUpdatedAfter": "2018-06-16T00:36:44.3345758Z",
        "lastUpdatedBefore": "2026-01-16T00:49:48.3686473Z",
        "orderBy": [
            {
                "order": "ASC",
                "orderBy": "RunEnd"
            }
        ]
    }
    runs = read_paginated_data_post(runs_url, data=data, headers=headers)
    
    pipeline_runs = {}

    if runs:
        for run in runs:
            pipeline_runs[run['pipelineName']] = run['runStart']

    else:
        raise Exception(f"Error retrieving pipelines")

    return pipeline_runs

# Function to get a list of notebooks
def get_notebooks():
    notebooks_url = f'{base_url}notebooks?api-version=2020-12-01'
    #print(f"Reading from {notebooks_url}")
    headers = {'Authorization': f'Bearer {token}'}
    notebooks = read_paginated_data(notebooks_url, headers=headers)
    
    if notebooks:
        return [notebook['name'] for notebook in notebooks]
    else:
        raise Exception(f"Error retrieving notebooks")

def findNode(node, name, maxLevel=-1) -> Node:
    if (maxLevel > 0) :
        foundNode = findall(node, maxlevel=maxLevel, filter_=lambda node: name == node.name)
    else:
        foundNode = findall(node, filter_=lambda node: name == node.name)

    if len(foundNode) == 0:
        return None
    else:
        return foundNode[0]

def duplicate_node(node, new_parent):
    # Create a new node with the same name and properties
    new_node = Node(node.name, parent=new_parent, itemType=node.__dict__.get('itemType', ''), itemSource="DUPLICATE")
    
    # Recursively duplicate children
    for child in node.children:
        duplicate_node(child, new_parent)
    return new_node

# Function to get all pipeline names and their notebook references
def get_pipeline_references():
    pipeline_runs = get_pipeline_runs()
    pipelines_url = f'{base_url}pipelines?api-version=2020-12-01'
    headers = {'Authorization': f'Bearer {token}'}
    pipelines = read_paginated_data(pipelines_url, headers=headers)
    
    print("Reading pipelines and notebooks")
    if pipelines:

        #build the initial tree, things will need to be moved
        root = Node(workspace_name, itemType="WORKSPACE")
        for pipeline in pipelines:
            pipeline_name = pipeline['name']
            pipeline_definition_url = f'{base_url}pipelines/{pipeline_name}?api-version=2021-06-01'
            pipeline_def_response = requests.get(pipeline_definition_url, headers=headers)
            
            if pipeline_def_response.status_code == 200:
                pipeline_definition = pipeline_def_response.json()
                level1Node = None
                
                foundNode = findNode(root, pipeline_name)
                if foundNode is None:
                    #this pipeline doesn't already exist
                    if pipeline_name in pipeline_runs:
                        lastRun = pipeline_runs[pipeline_name]
                    else:
                        lastRun = ""

                    level1Node = Node(pipeline_name, parent=root, itemType="PIPELINE", lastRunTime=lastRun)

                if level1Node is not None:

                    pipeline_jsonpath_expr = parse('$..pipeline.referenceName')
                    pipeline_matches = pipeline_jsonpath_expr.find(pipeline_definition)

                    #get a list of the pipelines and add them to the tree
                    for pipelineMatch in pipeline_matches:
                        pipelineName = pipelineMatch.value
                        foundNode = findNode(level1Node, pipelineName)
                        if foundNode is None:
                            #add a new node for pipeline
                            level2Node = Node(pipelineName, parent=level1Node, itemType="PIPELINE")

                    notebook_jsonpath_expr = parse('$..notebook.referenceName')
                    notebook_matches = notebook_jsonpath_expr.find(pipeline_definition)
                    
                    #get a list of the notebooks and add them to the tree
                    for notebook in notebook_matches:
                        foundNode = findNode(level1Node, str(notebook.value))
                        if foundNode is None:
                            level2Node = Node(notebook.value, parent=level1Node, itemType="NOTEBOOK")

            else:
                print("FAILED TO READ PIPELINES")


        ##TODO - This needs to recurse?

        #go through the tree. We need to go through each PIPLINE leaf node and find the corresponding node with all of the children and glue it on 
        #find all leaf nodes where the parents is not root
        for leafNode in list(PreOrderIter(root, filter_=lambda node: (node.is_leaf and node.height >= 0 and node.__dict__.get('itemType', '') == 'PIPELINE'))):
            foundNode = findNode(root, str(leafNode.name), 0)
            if foundNode is not None and foundNode != leafNode:
                print('**************** Looking at the found node ***************')
                print(f"{RenderTree(foundNode, maxlevel=3)}")
                print('**************** End of looking at the found node ***************')
                #copy the found node into the parent
                duplicate_node(foundNode, leafNode.parent)
                #remove leafNode
                leafNode.parent = None
            else:
                print(f"Could not find node for {leafNode.name}")
    else:
        raise Exception(f"Error retrieving pipelines")
    return root

root = get_pipeline_references()
for pre, fill, node in RenderTree(root):
    print(f"{pre} {node.name} ({node.__dict__.get('itemType', '')}) {node.__dict__.get('lastRunTime', '')} {node.__dict__.get('itemSource', '')}")