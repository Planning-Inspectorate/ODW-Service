-- Create e2e_test_results table in logging database
-- This table stores the results of end-to-end test framework runs

-- Create the logging database if it doesn't exist
CREATE DATABASE IF NOT EXISTS logging;

-- Drop table if exists (for clean recreation)
-- DROP TABLE IF EXISTS logging.e2e_test_results;

-- Create the e2e_test_results table
CREATE TABLE IF NOT EXISTS logging.e2e_test_results (
    entity STRING COMMENT 'The entity being tested (e.g., appeal-has)',
    std_count BIGINT COMMENT 'Count of records in standardised table',
    hrm_count BIGINT COMMENT 'Count of records in harmonised table', 
    hrm_active_count BIGINT COMMENT 'Count of active records in harmonised table',
    cur_count BIGINT COMMENT 'Count of records in curated table',
    cur_distinct_count BIGINT COMMENT 'Count of distinct records in curated table based on primary key',
    std_to_hrm_match BOOLEAN COMMENT 'Whether standardised and harmonised counts match',
    hrm_to_cur_match BOOLEAN COMMENT 'Whether harmonised active and curated counts match',
    cur_unique_check BOOLEAN COMMENT 'Whether curated table has unique primary keys',
    std_hrm_diff BIGINT COMMENT 'Difference between standardised and harmonised counts',
    hrm_cur_diff BIGINT COMMENT 'Difference between harmonised active and curated counts', 
    test_status STRING COMMENT 'Overall test status: Passed or detailed error message',
    test_timestamp TIMESTAMP COMMENT 'Timestamp when the test was executed'
)
USING DELTA
LOCATION 'abfss://logging@pinssynspodwdevuks.dfs.core.windows.net/e2e_test_results'
COMMENT 'End-to-end test results for data pipeline validation';

-- Verify table creation
DESCRIBE EXTENDED logging.e2e_test_results;
