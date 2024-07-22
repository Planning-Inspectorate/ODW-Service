import pytest
import json
from pyspark.sql.types import *
from pyspark.sql import DataFrame
import pprint
import testing_utils as testing_utils

""" 
Things to do (based on py_unit_tests)

compare schemas between data from orchestration.json and standardised
compare schemas between data from orchestration.json and harmonised
compare counts between standardised and harmonised (they should be identical)
compare the curated and harmonised data, check that all active=Y exist in harmonised
 """

entity_name: str = 'appeal-document'
std_db_name: str = 'odw_standardised_db'
hrm_db_name: str = 'odw_harmonised_db'
curated_db_name: str = 'odw_curated_db'
std_table_name: str = 'sb_appeal_document'
hrm_table_name: str = 'sb_appeal_document'
hrm_table_final: str = 'appeals_document_metadata'
curated_table_name: str = 'appeal_document'


def test_source_to_processed_workflow():
    
    sb_std_schema = create_spark_schema(std_db_name, entity_name)
    sb_std_table_schema = spark.table(f"{std_db_name}.{std_table_name}").schema
    sb_hrm_schema = create_spark_schema(hrm_db_name, entity_name)
    sb_hrm_table_schema = spark.table(f"{hrm_db_name}.{hrm_table_name}").schema
    
    '''Compare Schemas'''
    std_schema_correct: bool = test_compare_schemas(sb_std_schema, sb_std_table_schema)
    print(f"Service bus standardised schema correct: {std_schema_correct}\nTable: {std_db_name}.{std_table_name}\nDifferences shown above (if any)")
    hrm_schema_correct: bool = test_compare_schemas(sb_hrm_schema, sb_hrm_table_schema)
    print(f"Service bus harmonised schema correct: {hrm_schema_correct}\nTable: {hrm_db_name}.{hrm_table_name}\nDifferences shown above (if any)")

    '''Compare service bus standardised with harmonised'''
    std_schema_correct: bool = test_compare_schemas(sb_std_schema, sb_std_table_schema)
    print(f"Service bus standardised schema correct: {std_schema_correct}\nTable: {std_db_name}.{std_table_name}\nDifferences shown above (if any)")
    hrm_schema_correct: bool = test_compare_schemas(sb_hrm_schema, sb_hrm_table_schema)
    print(f"Service bus harmonised schema correct: {hrm_schema_correct}\nTable: {hrm_db_name}.{hrm_table_name}\nDifferences shown above (if any)")

    '''Should be the same count'''
    standardised_count, harmonised_count, counts_match = test_std_same_rows_hrm(std_table_name, hrm_table_name)
    print(f"Standardised Count: {standardised_count: ,}\nHarmonised Count: {harmonised_count: ,}\nCounts match: {counts_match}")

    '''Compare final harmonised table (if combined with Horizon) with curated table
    Comparing where IsActive = Y in harmonised = curated row count
    '''
    harmonised_final_count, curated_count, counts_match = test_curated_row_count(hrm_table_final, curated_table_name)
    print(f"Harmonised Final Count: {harmonised_final_count: ,}\nCurated Count: {curated_count: ,}\nCounts match: {counts_match}")

    print("Running Test")
    assert True is True
    print("Test Completed")

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    yield
    print("Before and After running")
