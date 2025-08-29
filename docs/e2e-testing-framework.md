# ODW End-to-End Testing Framework Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Test Execution Flow](#test-execution-flow)
5. [Data Validation Logic](#data-validation-logic)
6. [Pipeline Automation](#pipeline-automation)
7. [Result Validation and Analysis](#result-validation-and-analysis)
8. [Usage Instructions](#usage-instructions)
9. [Troubleshooting](#troubleshooting)

## Overview

The ODW (Operational Data Warehouse) End-to-End Testing Framework is a comprehensive data validation system designed to ensure data integrity and consistency across all layers of the data pipeline architecture. The framework automatically validates that data flows correctly from standardised through harmonised to curated data layers.

### Key Features

- **Automated Data Validation**: Validates data consistency across standardised, harmonised, and curated layers
- **Entity-Agnostic Testing**: Works with any entity configured in the orchestration system
- **Count-Based Validation**: Performs row count comparisons and data integrity checks
- **Detailed Result Logging**: Stores comprehensive test results with timestamps and detailed status messages
- **CI/CD Integration**: Integrates seamlessly with Azure DevOps for nightly automated testing
- **Real-time Monitoring**: Provides immediate feedback on data pipeline health

### Testing Scope

The framework validates the following data integrity aspects:
- **Standardised to Harmonised**: Ensures all standardised records are properly processed to harmonised
- **Harmonised to Curated**: Validates that active harmonised records match curated records
- **Curated Uniqueness**: Checks that curated data maintains uniqueness based on primary keys
- **Data Completeness**: Ensures no data loss during transformation processes

## Architecture

The E2E testing framework follows a multi-layered architecture that mirrors the ODW data processing pipeline:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Standardised   │───▶│   Harmonised     │───▶│    Curated      │
│     Layer       │    │     Layer        │    │     Layer       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                    ┌──────────────────────────┐
                    │   E2E Test Framework     │
                    │  (df_e2e_test_framework) │
                    └──────────────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │   Test Results Storage   │
                    │  (logging.e2e_test_     │
                    │       _results)          │
                    └──────────────────────────┘
```

### Data Flow Architecture

1. **Source Layer**: Reads from standardised, harmonised, and curated databases
2. **Processing Layer**: Performs data aggregation and comparison logic
3. **Validation Layer**: Applies business rules and generates test results
4. **Storage Layer**: Persists results to the logging database for analysis

## Core Components

### 1. Master Test Pipeline (`pln_master_test`)

The central orchestration pipeline that coordinates testing across all enabled entities.

**Location**: `workspace/pipeline/pln_master_test.json`

**Key Functions**:
- Queries the configuration database to get all enabled Service Bus entities
- Excludes specific entities that have specialized handling
- Orchestrates sequential testing across all entities
- Dynamically configures table names and primary keys for each entity

**Configuration Query**:
```sql
SELECT STRING_AGG(entity_name, ',') AS entities
FROM [odw_config_db].[dbo].[main_pipeline_config]
WHERE is_enabled = 1
AND System_name = 'Service bus'
AND entity_name NOT IN ('appeal-document', 'appeal-s78', 'appeal-event', 
                        'entraid', 'nsip-document', 'nsip-exam-timetable', 
                        'nsip-project', 'nsip-project-update','s51-advice', 
                        'nsip-representation')
```

### 2. E2E Test Data Flow (`df_e2e_test_framework`)

The core data processing component that performs the actual validation logic.

**Location**: `workspace/dataflow/df_e2e_test_framework.json`

**Data Sources**:
- **StandardisedSource**: Reads from `odw_standardised_db` tables
- **HarmonisedSource**: Reads from `odw_harmonised_db` tables  
- **CuratedSource**: Reads from `odw_curated_db` tables

**Transformations**:
- **StandardisedCount**: Counts valid standardised records (non-null message_type and message_id)
- **HarmonisedCount**: Counts total and active harmonised records (IsActive = 'Y')
- **CuratedCount**: Counts total and distinct curated records based on primary key
- **TestResults**: Generates comprehensive test status with detailed error messages

### 3. Test Results Table (`logging.e2e_test_results`)

Central storage for all test execution results.

**Schema**:
```sql
CREATE TABLE logging.e2e_test_results (
    entity STRING,                    -- Entity being tested (e.g., 'appeal-has')
    std_count BIGINT,                -- Count of records in standardised table
    hrm_count BIGINT,                -- Count of records in harmonised table
    hrm_active_count BIGINT,         -- Count of active records in harmonised table
    cur_count BIGINT,                -- Count of records in curated table
    cur_distinct_count BIGINT,       -- Count of distinct records in curated table
    std_to_hrm_match BOOLEAN,        -- Whether standardised and harmonised counts match
    hrm_to_cur_match BOOLEAN,        -- Whether harmonised active and curated counts match
    cur_unique_check BOOLEAN,        -- Whether curated table has unique primary keys
    std_hrm_diff BIGINT,            -- Difference between standardised and harmonised
    hrm_cur_diff BIGINT,            -- Difference between harmonised and curated
    test_status STRING,              -- Overall status: 'PASSED' or detailed error message
    test_timestamp TIMESTAMP         -- When the test was executed
)
```

### 4. Table Creation Notebook (`py_create_e2e_test_results_table`)

Utility notebook that creates and manages the test results table structure.

**Location**: `workspace/notebook/py_create_e2e_test_results_table.json`

**Functions**:
- Creates the logging database if it doesn't exist
- Creates the e2e_test_results table with proper schema
- Uses Delta Lake format for optimal performance and ACID compliance

## Test Execution Flow

### 1. Entity Discovery Phase
```
┌─────────────────────────────────────┐
│  Query main_pipeline_config         │
│  Filter: is_enabled = 1             │
│  System: Service bus                │
│  Exclude: Special entities          │
└─────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Build entity array                 │
│  Example: ['appeal-has',            │
│           'appeal-case',             │
│           'appeal-type']             │
└─────────────────────────────────────┘
```

### 2. Per-Entity Testing Phase
For each entity in the array:

```
┌─────────────────────────────────────┐
│  Lookup orchestration config        │
│  Get: std_table, hrm_table,         │
│       primary_key                   │
└─────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Execute df_e2e_test_framework      │
│  Parameters: entity_name, tables,   │
│             databases, primary_key  │
└─────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Store results in logging table     │
│  Include: counts, status, timestamp │
└─────────────────────────────────────┘
```

### 3. Validation Logic Flow

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Standardised    │  │ Harmonised      │  │ Curated         │
│ Data Source     │  │ Data Source     │  │ Data Source     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Count valid     │  │ Count total &   │  │ Count total &   │
│ records         │  │ active records  │  │ distinct        │
│ (message_type   │  │ (IsActive='Y')  │  │ (by primary_key)│
│  not null)      │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         └─────────┬───────────┼─────────────────────┘
                   ▼           ▼                     
         ┌─────────────────────────────────────────┐
         │           Cross Join & Compare          │
         │                                         │
         │  Tests:                                 │
         │  • std_count == hrm_count               │
         │  • hrm_active_count == cur_count        │
         │  • cur_count == cur_distinct_count      │
         └─────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │         Generate Test Status            │
         │                                         │
         │  PASSED: All validations pass           │
         │  FAILED: Detailed error messages        │
         │  Include: Specific count mismatches     │
         └─────────────────────────────────────────┘
```

## Data Validation Logic

### Validation Rules

The framework applies three primary validation rules:

#### 1. Standardised to Harmonised Consistency
```sql
std_count == hrm_count
```
- **Purpose**: Ensures no data loss during standardised to harmonised transformation
- **Logic**: Counts valid standardised records (non-null message_type and message_id) and compares with total harmonised records
- **Failure**: Indicates potential data processing issues in the harmonisation layer

#### 2. Harmonised to Curated Consistency  
```sql
hrm_active_count == cur_count
```
- **Purpose**: Validates that only active harmonised records are promoted to curated
- **Logic**: Counts harmonised records where IsActive='Y' and compares with curated record count
- **Failure**: Suggests issues with the curation process or active record filtering

#### 3. Curated Data Uniqueness
```sql
cur_count == cur_distinct_count
```
- **Purpose**: Ensures curated data maintains uniqueness based on primary key
- **Logic**: Compares total curated records with distinct count by primary key
- **Failure**: Indicates duplicate records in the curated layer

### Test Status Generation

The framework generates detailed status messages:

```sql
test_status = 
  CASE 
    WHEN (std_count == hrm_count) 
     AND (hrm_active_count == cur_count) 
     AND (cur_count == cur_distinct_count) 
    THEN 'PASSED'
    
    -- Multiple failures
    WHEN (std_count != hrm_count) 
     AND (hrm_active_count != cur_count) 
     AND (cur_count != cur_distinct_count)
    THEN 'FAILED: Standardised-Harmonised count mismatch (' + std_hrm_diff + '), 
                  Harmonised-Curated count mismatch (' + hrm_cur_diff + '), 
                  Curated uniqueness check failed'
    
    -- Specific combinations of failures...
    
  END
```

## Pipeline Automation

### Nightly Automation Pipelines

#### Development Environment
**Pipeline**: `nightly-data-validation-tests-dev.yaml`
- **Schedule**: Daily at 11 PM UTC (`0 23 * * *`)
- **Trigger**: Automatic, no manual triggers
- **Branch**: main

#### Test Environment  
**Pipeline**: `nightly-data-validation-tests-test.yaml`
- **Schedule**: Daily at 11 PM UTC (`0 23 * * *`)
- **Trigger**: Automatic, no manual triggers
- **Branch**: main

### Pipeline Stages

#### Stage 1: Run E2E Tests
```yaml
stages:
- template: stages/run-e2e-tests.yaml
  parameters:
    agentPool: ${{ variables.agentPool }}
    env: ${{ variables.env }}
```

#### Stage 2: Execute Tests Job
```bash
# Run pytest against the pln_master_test pipeline
python3 -m pytest tests/e2e_test/test_e2e_pln_master_test.py::TestE2EPlnMasterTest::test_pln_master_test_pipeline -vv -rP --junitxml=e2e-test-results.xml

# Validate test results using SynapseUtil
python3 tests/e2e_test/validate_e2e_results.py ${{ env }}
```

### Test Execution Process

1. **Pipeline Trigger**: Triggered by pytest framework
2. **Pipeline Execution**: Runs `pln_master_test` pipeline in Synapse
3. **Result Generation**: Pipeline writes results to `logging.e2e_test_results`
4. **Result Validation**: Python script validates all tests passed
5. **Status Reporting**: Generates JUnit XML for Azure DevOps integration

## Result Validation and Analysis

### Validation Script (`validate_e2e_results.py`)

The validation script provides comprehensive result analysis:

**Key Features**:
- Connects to Synapse serverless SQL pool
- Queries recent test results (configurable time window)
- Provides detailed result analysis and metrics
- Exits with appropriate status codes for CI/CD integration

**Usage**:
```bash
python3 validate_e2e_results.py [environment]
```

**Example Output**:
```
Fetching E2E Tests results...
====================================================
Environment: dev
Database: logging
Looking back: 2 hours
Max wait time: 10 minutes

Found 5 E2E test result(s)!

Test Results Summary:
==================================================
[PASS] Entity: appeal-has, Status: PASSED, Time: 2024-08-29 13:45:23
  std_count: 1250
  hrm_count: 1250
  hrm_active_count: 1200
  cur_count: 1200
  std_to_hrm_match: True
  hrm_to_cur_match: True
  cur_unique_check: True

[FAIL] Entity: appeal-case, Status: FAILED: Standardised-Harmonised count mismatch (-5), Time: 2024-08-29 13:45:25
  std_count: 850
  hrm_count: 855
  hrm_active_count: 830
  cur_count: 830
  std_to_hrm_match: False
  hrm_to_cur_match: True
  cur_unique_check: True

==================================================
Summary: 2 entities tested
Entities: appeal-case, appeal-has

FAILURE: One or more E2E tests FAILED!

E2E Test Verification: FAILED
```

### Result Analysis

#### Success Indicators
- **Status**: All entities show `PASSED` status
- **Count Consistency**: All count comparisons match
- **No Data Loss**: Differences between layers are zero

#### Failure Analysis
Common failure patterns and their meanings:

1. **Standardised-Harmonised Mismatch**:
   - **Symptom**: `std_count != hrm_count`
   - **Possible Causes**: Processing failures, incomplete harmonisation, data quality issues
   - **Investigation**: Check harmonisation pipeline logs, validate source data

2. **Harmonised-Curated Mismatch**:
   - **Symptom**: `hrm_active_count != cur_count`  
   - **Possible Causes**: Curation pipeline issues, IsActive flag problems, filtering logic errors
   - **Investigation**: Review curation logic, check IsActive values

3. **Curated Uniqueness Failure**:
   - **Symptom**: `cur_count != cur_distinct_count`
   - **Possible Causes**: Duplicate primary keys, merge logic issues
   - **Investigation**: Query curated tables for duplicates, review merge/upsert logic

## Usage Instructions

### Manual Test Execution

#### 1. Run Individual Entity Test

```python
# In Synapse Analytics Studio
# Navigate to: Develop > Pipelines > pln_master_test
# Click "Debug" or "Add trigger" > "Trigger now"
```

#### 2. Monitor Test Execution

```sql
-- Query recent test results
SELECT entity, test_status, test_timestamp,
       std_count, hrm_count, hrm_active_count, cur_count
FROM logging.e2e_test_results 
WHERE test_timestamp >= DATEADD(hour, -2, GETDATE())
ORDER BY test_timestamp DESC
```

#### 3. Validate Results Programmatically

```bash
# From project root
cd tests/e2e_test
python3 validate_e2e_results.py dev  # or 'test' for test environment
```

### Adding New Entities

To include a new entity in E2E testing:

1. **Enable in Configuration**:
```sql
UPDATE [odw_config_db].[dbo].[main_pipeline_config] 
SET is_enabled = 1 
WHERE entity_name = 'your-new-entity'
AND System_name = 'Service bus'
```

2. **Configure Orchestration**:
```sql
-- Ensure orchestration table has entry
SELECT * FROM orchestration 
WHERE Source_Frequency_Folder = 'your-new-entity'
```

3. **Verify Table Structure**:
- Standardised table has `message_type` and `message_id` columns
- Harmonised table has `IsActive` column  
- Curated table has defined primary key

### Excluding Problematic Entities

To temporarily exclude entities from testing:

```sql
-- Option 1: Disable in main config
UPDATE [odw_config_db].[dbo].[main_pipeline_config] 
SET is_enabled = 0 
WHERE entity_name = 'problematic-entity'

-- Option 2: Add to exclusion list in pipeline
-- Edit pln_master_test.json Lookup_main_pipeline_config activity
-- Add entity to NOT IN clause
```

## Troubleshooting

### Common Issues

#### 1. No Test Results Found

**Symptoms**:
- Validation script reports "No test results found"
- Empty results from logging table

**Solutions**:
- Check if `pln_master_test` pipeline completed successfully
- Verify logging database connectivity
- Confirm `e2e_test_results` table exists and is accessible
- Check for entity configuration issues

**Investigation Query**:
```sql
-- Check if table exists and has data
SELECT COUNT(*) as total_rows,
       MAX(test_timestamp) as latest_test
FROM logging.e2e_test_results
```

#### 2. Pipeline Execution Failures

**Symptoms**:
- `pln_master_test` pipeline fails
- Entity lookup failures
- Data flow execution errors

**Solutions**:
- Check orchestration table completeness
- Verify database connectivity
- Validate entity configuration
- Review pipeline execution logs

**Investigation Steps**:
1. Check pipeline run history in Synapse Studio
2. Review data flow execution details
3. Validate source table accessibility

#### 3. Inconsistent Test Results

**Symptoms**:
- Tests pass sometimes, fail other times
- Count mismatches without data changes
- Timing-related failures

**Solutions**:
- Check for concurrent data processing
- Verify data freshness and completeness
- Review pipeline execution timing
- Consider data processing delays

### Debugging Queries

#### Check Entity Configuration
```sql
SELECT entity_name, is_enabled, System_name
FROM [odw_config_db].[dbo].[main_pipeline_config]
WHERE System_name = 'Service bus'
ORDER BY entity_name
```

#### Verify Orchestration Setup
```sql
SELECT Source_Frequency_Folder, 
       Standardised_Table_Name,
       Harmonised_Table_Name,
       Entity_Primary_Key
FROM orchestration
WHERE Source_Frequency_Folder IN (
    SELECT entity_name 
    FROM [odw_config_db].[dbo].[main_pipeline_config]
    WHERE is_enabled = 1 AND System_name = 'Service bus'
)
```

#### Analyze Test Result Trends
```sql
SELECT entity,
       test_status,
       COUNT(*) as occurrence_count,
       MIN(test_timestamp) as first_occurrence,
       MAX(test_timestamp) as latest_occurrence
FROM logging.e2e_test_results
WHERE test_timestamp >= DATEADD(day, -7, GETDATE())
GROUP BY entity, test_status
ORDER BY entity, occurrence_count DESC
```

#### Check Data Layer Counts
```sql
-- Example for appeal-has entity
-- Standardised layer
SELECT COUNT(*) as std_count 
FROM odw_standardised_db.appeal_has 
WHERE message_type IS NOT NULL AND message_id IS NOT NULL

-- Harmonised layer  
SELECT COUNT(*) as hrm_total,
       SUM(CASE WHEN IsActive = 'Y' THEN 1 ELSE 0 END) as hrm_active
FROM odw_harmonised_db.sb_appeal_has

-- Curated layer
SELECT COUNT(*) as cur_total,
       COUNT(DISTINCT appealId) as cur_distinct
FROM odw_curated_db.appeal_has
```

### Performance Considerations

#### Optimization Tips

1. **Compute Resources**: Use appropriate Spark pool sizes for data flow execution
2. **Data Partitioning**: Consider partitioning strategies for large tables  
3. **Query Optimization**: Optimize count queries with appropriate indexes
4. **Concurrent Execution**: Avoid running tests during heavy data processing periods

#### Monitoring Recommendations

1. **Set up alerts** for test failures in Azure DevOps
2. **Monitor execution times** to identify performance degradation
3. **Track result trends** to identify systemic issues
4. **Review resource utilization** during test execution

---

*This documentation covers the complete ODW End-to-End Testing Framework. For additional support or questions, please refer to the development team or create an issue in the project repository.*
