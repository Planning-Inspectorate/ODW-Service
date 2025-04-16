import pytest
import pipelineutils
import constants
import warnings

def test_nsip_s51_advice_notebook(credential_name, azure_credential, synapse_endpoint: str):

    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    # run the testing notebook
    notebookname: str = "py_unit_tests_nsip_s51_advice"
    
    notebook_raw_params = {
        "sparkPool": "pinssynspodwpr",
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
                "value": "s51-advice"
            },
            "folder_name": {
                "type": "String",
                "value": "s51-advice"
            },
            "std_db_name": {
                "type": "String",
                "value": "odw_standardised_db"
            },
            "hrm_db_name": {
                "type": "String",
                "value": "odw_harmonised_db"
            },
            "curated_db_name": {
                "type": "String",
                "value": "odw_curated_db"
            },
            "std_table_name": {
                "type": "String",
                "value": "sb_s51_advice"
            },
            "horizon_std_table_name": {
                "type": "String",
                "value": "horizon_nsip_advice"
            },
            "hrm_table_name": {
                "type": "String",
                "value": "sb_s51_advice"
            },
            "hrm_table_final": {
                "type": "String",
                "value": "nsip_s51_advice"
            },
            "curated_table_name": {
                "type": "String",
                "value": "s51_advice"
            },
            "curated_db_migration_name": {
                "type": "String",
                "value": "odw_curated_migration_db"
            },
            "curated_table_migration_name": {
                "type": "String",
                "value": "s51_advice"
            },
            "primary_key": {
                "type": "String",
                "value": "adviceId"
            },
        }
    }

    #run the notebook
    (notebook_run_result, exitMessage) = pipelineutils.run_and_observe_notebook(credential_name, azure_credential, synapse_endpoint, notebookname, notebook_raw_params)
    print("Notebook response *" +str(exitMessage) +"*")
    assert notebook_run_result == constants.NOTEBOOK_SUCCESS_STATUS 
    assert exitMessage == constants.NOTEBOOK_EXIT_CODE_SUCCESS
    print("test_nsip_s51_advice Completed")

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    print("Before and After running")