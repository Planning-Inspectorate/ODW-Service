import pytest
import pipelineutils
import constants
import warnings

def test_function_gets62(credential_name, azure_credential, synapse_endpoint: str):
    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    # run the pipeline
    pipelinename: str = "pln_run_function_app_unit_test"
    
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
        },
        "parameters": {
            "function_name": [
                 "gets62"
            ]
        }
    }
    

    #run the pipeline
    pipeline_run_result = pipelineutils.run_and_observe_pipeline(credential_name, azure_credential, synapse_endpoint, pipelinename, pipeline_raw_params)
    assert pipeline_run_result == constants.PIPELINE_SUCCESS_STATUS
    print("test_function_gets62_pipeline Completed")


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    print("Before and After running")
