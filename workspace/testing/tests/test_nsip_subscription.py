import pytest
import pipelineutils
from constants import NOTEBOOK_EXIT_CODE_SUCCESS, NOTEBOOK_SUCCESS_STATUS
from warnings import filterwarnings

def test_nsip_project_notebook(credential_name, azure_credential, synapse_endpoint: str):

    filterwarnings("ignore", category=DeprecationWarning) 

    # run the testing notebook
    notebookname: str = "py_unit_tests_nsip_subscription"
    
    notebook_raw_params = {
        "sparkPool": "tempsparkpool",
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
            "entity_name": { "type": "String", "value": "nsip-subscription" },
            "std_db_name": { "type": "String", "value": "odw_standardised_db" },
            "hrm_db_name": { "type": "String", "value": "odw_harmonised_db" },
            "curated_db_name": { "type": "String", "value": "odw_curated_db" },
            "std_table_name": { "type": "String", "value": "sb_nsip_subscription" },
            "hrm_table_name": { "type": "String", "value": "sb_nsip_subscription" },
            "curated_table_name": { "type": "String", "value": "nsip_subscription" },
        }
    }

    #run the notebook
    (notebook_run_result, exitMessage) = pipelineutils.run_and_observe_notebook(credential_name, azure_credential, synapse_endpoint, notebookname, notebook_raw_params)
    print("Notebook response *" +str(exitMessage) +"*")
    assert notebook_run_result == NOTEBOOK_SUCCESS_STATUS 
    assert exitMessage == NOTEBOOK_EXIT_CODE_SUCCESS
    print("test_nsip_subscription Completed")

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    print("Before and After running")

