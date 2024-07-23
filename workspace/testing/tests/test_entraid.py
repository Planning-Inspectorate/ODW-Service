import pytest
import pipelineutils
import constants

def test_source_to_processed_workflow(azure_credential,
                                 synapse_endpoint: str,
                                 pipeline_name: str):
    
    # run the testing notebook
    #notebookname: str = "py_unit_tests"
    notebookname: str = "zendesk_read_me"
    
    # Trigger the Master Pipeline for Landing to Raw Zone
    notebook_raw_params = {
        "sparkPool": "exampleSparkpool",
        "notebook": notebookname,
        "parameters": {
            "entity_name": {
               "type": "String",
               "value": "appeal-document",
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
               "value": "sb_appeal_document",
            },
            "hrm_table_name": {
               "type": "String",
               "value": "sb_appeal_document",
            },
            "hrm_table_final": {
               "type": "String",
               "value": "appeals_document_metadata",
            },
            "curated_table_name": {
               "type": "String",
               "value": "appeal_document",
            }
        }
    }

    print(f"{notebookname} Notebook Raw Parameters : {notebook_raw_params}\n")
    #run the notebook
    notebook_run_result = pipelineutils.run_and_observe_notebook(azure_credential, synapse_endpoint, pipeline_name, notebook_raw_params)

    assert notebook_run_result == constants.NOTEBOOK_SUCCESS_STATUS

    print("Running Test")
    assert True is True
    print("Test Completed")

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    print("Before and After running")
