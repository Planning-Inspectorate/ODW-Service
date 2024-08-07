import pytest
import pipelineutils
import constants
import warnings

def test_entraid_pipeline(credential_name, azure_credential, synapse_endpoint: str):
    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    #list the pipelines out
    #pipelineutils.list_pipelines(credential_name, azure_credential, synapse_endpoint)

    # run the pipeline
    pipelinename: str = "rel_1262_entra_id"
    
    pipeline_raw_params = {
        "sparkPool": "pinssynspodw",
        "pipeline": pipelinename,
        "sessionOptions": {
            "driverMemory": "28g",
            "driverCores": 4,
            "executorMemory": "28g",
            "executorCores": 4,
            "numExecutors": 2,
            "runAsWorkspaceSystemIdentity": False
        }
    }

    #run the pipeline
    pipeline_run_result = pipelineutils.run_and_observe_pipeline(credential_name, azure_credential, synapse_endpoint, pipelinename, pipeline_raw_params)
    assert pipeline_run_result == constants.PIPELINE_SUCCESS_STATUS
    print("test_entraid_pipeline Completed")


def test_entraid_notebook(credential_name, azure_credential, synapse_endpoint: str):

    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    # run the testing notebook
    notebookname: str = "py_unit_tests"
    
    # Trigger the Master Pipeline for Landing to Raw Zone
    notebook_raw_params = {
        "sparkPool": "pinssynspodw",
        "notebook": notebookname,
        "sessionOptions": {
            "driverMemory": "28g",
            "driverCores": 4,
            "executorMemory": "28g",
            "executorCores": 4,
            "numExecutors": 2,
            "runAsWorkspaceSystemIdentity": False
        },
        "parameters": {
            "entity_name": {
               "type": "String",
               "value": "entraid",
            },
            "std_db_name": {
               "type": "String",
               "value": "odw_standardised_db",
            },
            "hrm_db_name": {
               "type": "String",
               "value": "odw_harmonised_db",
            },
            "curated_db_name": {
               "type": "String",
               "value": "odw_curated_db",
            },
            "std_table_name": {
               "type": "String",
               "value": "entraid",
            },
            "hrm_table_name": {
               "type": "String",
               "value": "entraid",
            },
            "isServiceBusSchema": {
               "type": "Boolean",
               "value": "False",
            }
        }
    }

    #run the notebook
    (notebook_run_result, exitMessage) = pipelineutils.run_and_observe_notebook(credential_name, azure_credential, synapse_endpoint, notebookname, notebook_raw_params)
    print("Notebook response *" +str(exitMessage) +"*")
    assert notebook_run_result == constants.NOTEBOOK_SUCCESS_STATUS 
    assert exitMessage == constants.NOTEBOOK_EXIT_CODE_SUCCESS
    print("test_entraid_notebook Completed")

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    print("Before and After running")
