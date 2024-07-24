import requests
import datetime
import time
import json
from azure.synapse.artifacts import ArtifactsClient
from azure.identity import ClientSecretCredential
import constants
import uuid
import pipelineutils


def run_and_observe_pipeline(azure_credential: ClientSecretCredential,
                             synapse_endpoint: str, pipeline_name: str,
                             params: dict):
    synapse_client: ArtifactsClient = ArtifactsClient(
        azure_credential, synapse_endpoint)
    if params is not None:
        pipeline_run_id = _run_pipeline(
            azure_credential, synapse_endpoint, pipeline_name, params)
    else:
        pipeline_run_id = _run_pipeline(
            azure_credential, synapse_endpoint, pipeline_name)
    print(f'PIPELINE RUNNING WITH RunID: {pipeline_run_id}\n')
    pipeline_run_status = observe_pipeline(synapse_client, pipeline_run_id)
    return pipeline_run_status


def _run_pipeline(azure_credential: ClientSecretCredential,
                  synapse_endpoint: str, pipeline_name: str,
                  params: dict) -> str:
    print(f'RUNNING PIPELINE {pipeline_name}...\n')
    # Implementation with SDK
    # run_pipeliine = synapse_client.pipeline.create_pipeline_run(
    #     pipeline_name, parameters=params_for_pipeline)
    # print(run_pipeliine.run_id)
    # Implementation with REST API
    run_pipeline_url = f'{synapse_endpoint}/pipelines/{pipeline_name}'\
        '/createRun?api-version=2020-12-01'
    access_token = azure_credential.get_token(
        constants.AZURE_SYNAPSE_ENDPOINT)
    headers = {'Authorization': f'Bearer {access_token.token}'}
    response = requests.post(run_pipeline_url, headers=headers,
                             data=json.dumps(params))
    pipeline_run_id = response.json()['runId']
    return pipeline_run_id


def observe_pipeline(synapse_client: ArtifactsClient, run_id: str,
                     until_status=["Succeeded", "TimedOut",
                                   "Failed", "Cancelled"],
                     poll_interval=15) -> str:
    print('OBSERVING PIPELINE RUN...\n')
    pipeline_run_status = ""
    while(pipeline_run_status not in until_status):
        now = datetime.datetime.now()
        print(
            f'{now.strftime("%Y-%m-%d %H:%M:%S")}'
            f' Polling pipeline with run id {run_id}'
            f' for status in {", ".join(until_status)}')
        pipeline_run = synapse_client.pipeline_run.get_pipeline_run(run_id)
        pipeline_run_status = pipeline_run.status
        time.sleep(poll_interval)
    print(
        f'pipeline run id {run_id}'
        f'finished with status {pipeline_run_status}\n')
    return pipeline_run_status



def run_and_observe_notebook(azure_credential: ClientSecretCredential,
                             synapse_endpoint: str, notebook_name: str,
                             params: dict):
    synapse_client: ArtifactsClient = ArtifactsClient(azure_credential, synapse_endpoint)
    if params is not None:
        notebook_run_id = _run_notebook(azure_credential, synapse_endpoint, notebook_name, params)
    else:
        notebook_run_id = _run_notebook(azure_credential, synapse_endpoint, notebook_name)
    print(f'notebook RUNNING WITH RunID: {notebook_run_id}\n')
    notebook_run_status, exitMessage = observe_notebook(azure_credential, synapse_endpoint, notebook_run_id)
    return (notebook_run_status, exitMessage)


def _run_notebook(azure_credential: ClientSecretCredential,
                  synapse_endpoint: str, notebook_name: str,
                  params: dict) -> str:
    print(f'RUNNING notebook {notebook_name}...\n')
    # Implementation with REST API
    notebook_run_id:str = str(uuid.uuid4())
    run_notebook_url = f'{synapse_endpoint}/notebooks/runs/{notebook_run_id}?api-version=2022-03-01-preview'
    access_token = azure_credential.get_token(constants.AZURE_SYNAPSE_ENDPOINT)
    headers = {'Authorization': f'Bearer {access_token.token}'}
    response = requests.post(run_notebook_url, headers=headers,data=json.dumps(params))
    return notebook_run_id


#Logs are available here : https://portal.azure.com/#view/Microsoft_Azure_Monitoring/AzureMonitoringBrowseBlade/~/logs
#query is 
#   search in (SynapseGatewayApiRequests) "<runid>" 

def observe_notebook(azure_credential: ClientSecretCredential,
                     synapse_endpoint: str, 
                     notebook_run_id: str,
                     until_status=["Succeeded", "TimedOut",
                                   "Failed", "Cancelled"],
                     poll_interval=15) -> str:
    print('OBSERVING notebook RUN...\n')
    notebook_run_status = ""
    while(notebook_run_status not in until_status):
        now = datetime.datetime.now()
        print(f'{now.strftime("%Y-%m-%d %H:%M:%S")}'f' Polling notebook with run id {notebook_run_id}'f' for status in {", ".join(until_status)}')
        run_notebook_url = f'{synapse_endpoint}/notebooks/runs/{notebook_run_id}?api-version=2022-03-01-preview'
        access_token = azure_credential.get_token(constants.AZURE_SYNAPSE_ENDPOINT)
        headers = {'Authorization': f'Bearer {access_token.token}'}
        response = requests.post(run_notebook_url, headers=headers)
        if response.status_code == 200 : 
            print(response)
            notebook_run_status = response.json()['result']['runStatus']
            exitMessage = response.json()['result']['exitValue']
            time.sleep(poll_interval)
        else:
            print("Failed to check status " +str(response.status_code))
            return ("Failed", "")

    print(f'notebook run id {notebook_run_id}' f'finished with status {notebook_run_status}\n')
    return (notebook_run_status, exitMessage)