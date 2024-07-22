import pytest
import json

""" 
Things to do (based on py_unit_tests)

compare schemas between data from orchestration.json and standardised
compare schemas between data from orchestration.json and harmonised
compare counts between standardised and harmonised (they should be identical)
compare the curated and harmonised data, check that all active=Y exist in harmonised
 """


def test_source_to_processed_workflow():
    print("Running Test")
    assert True is True
    print("Test Completed")

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    print("Before and After running")
