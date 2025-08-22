#!/bin/bash
set -e

# Automated E2E Test Results Verification Script (Bash + curl)
#
# This script uses Azure CLI for authentication and curl for REST API calls
# to query the logging.e2e_test_results table in Synapse Analytics.
#
# Usage: ./verify-e2e-test-results.sh <workspace_name> [hours_back] [max_wait_minutes]
#
# Environment: Should be run within Azure CLI context (az login already done)

WORKSPACE_NAME="${1}"
HOURS_BACK="${2:-2}"
MAX_WAIT_MINUTES="${3:-10}"

if [ -z "$WORKSPACE_NAME" ]; then
    echo "ERROR: Workspace name is required"
    echo "Usage: $0 <workspace_name> [hours_back] [max_wait_minutes]"
    exit 2
fi

echo "Starting E2E Test Results Verification (Bash + curl)"
echo "Workspace: $WORKSPACE_NAME"
echo "Looking back: $HOURS_BACK hours"
echo "Max wait time: $MAX_WAIT_MINUTES minutes"
echo "--------------------------------------------------------"

# Get access token using Azure CLI
echo "Getting access token..."
ACCESS_TOKEN=$(az account get-access-token --resource https://dev.azuresynapse.net --query accessToken -o tsv)

if [ -z "$ACCESS_TOKEN" ]; then
    echo "ERROR: Failed to get access token"
    exit 2
fi

echo "Successfully obtained access token"

# Construct SQL query
SQL_QUERY="SELECT entity, test_status, test_timestamp, std_count, hrm_count, hrm_active_count, cur_count, std_to_hrm_match, hrm_to_cur_match, cur_unique_check FROM logging.e2e_test_results WHERE test_timestamp >= DATEADD(hour, -${HOURS_BACK}, GETDATE()) ORDER BY test_timestamp DESC"

# Construct serverless SQL endpoint
SQL_ENDPOINT="https://${WORKSPACE_NAME}-ondemand.sql.azuresynapse.net"

echo "Looking for E2E test results from the last $HOURS_BACK hours..."

START_TIME=$(date +%s)
MAX_WAIT_SECONDS=$((MAX_WAIT_MINUTES * 60))

while true; do
    echo "Executing SQL query against Synapse serverless pool..."
    
    # Try different approaches to execute the SQL query
    # Approach 1: Try REST API call
    RESPONSE=$(curl -s -X POST "${SQL_ENDPOINT}/sql/connections/master/query" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"${SQL_QUERY}\"}" \
        -w "HTTP_STATUS:%{http_code}" 2>/dev/null || echo "HTTP_STATUS:000")
    
    HTTP_STATUS=$(echo "$RESPONSE" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
    RESPONSE_BODY=$(echo "$RESPONSE" | sed 's/HTTP_STATUS:[0-9]*$//')
    
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "Query executed successfully"
        
        # Parse response and check for results
        if echo "$RESPONSE_BODY" | grep -q "\"entity\""; then
            echo "Found E2E test results!"
            
            # Check if all tests passed
            if echo "$RESPONSE_BODY" | grep -q "\"PASSED\""; then
                echo ""
                echo "Results found:"
                echo "$RESPONSE_BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, list):
        results = data
    elif 'results' in data:
        results = data['results']
    elif 'value' in data:
        results = data['value']
    else:
        results = [data]
    
    all_passed = True
    entities_tested = set()
    
    for row in results:
        entity = row.get('entity', 'Unknown')
        test_status = row.get('test_status', 'Unknown')
        entities_tested.add(entity)
        
        status_indicator = 'PASS' if test_status == 'PASSED' else 'FAIL'
        print(f'[{status_indicator}] Entity: {entity}, Status: {test_status}')
        
        if test_status != 'PASSED':
            all_passed = False
    
    print(f'\\nSummary: {len(entities_tested)} entities tested')
    print(f'Entities: {', '.join(sorted(entities_tested))}')
    
    if all_passed:
        print('SUCCESS: All E2E tests PASSED!')
        sys.exit(0)
    else:
        print('FAILURE: One or more E2E tests FAILED!')
        sys.exit(1)
        
except Exception as e:
    print(f'Error parsing results: {e}')
    print('Raw response:')
    print(sys.stdin.read())
    sys.exit(1)
" 2>/dev/null
                
                # Check the exit status of the Python script
                if [ $? -eq 0 ]; then
                    echo ""
                    echo "E2E Test Verification: PASSED"
                    exit 0
                else
                    echo ""
                    echo "E2E Test Verification: FAILED"
                    echo "The pipeline will fail to prevent false positive results."
                    exit 1
                fi
            else
                echo "No PASSED test results found in the response"
            fi
        else
            echo "No test results found in response"
        fi
    else
        echo "Query failed with HTTP status: $HTTP_STATUS"
        if [ "$HTTP_STATUS" != "000" ]; then
            echo "Response body: $RESPONSE_BODY"
        fi
    fi
    
    # Check if we should continue waiting
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -ge $MAX_WAIT_SECONDS ]; then
        echo "ERROR: No E2E test results found after waiting $MAX_WAIT_MINUTES minutes"
        echo ""
        echo "Manual Verification Instructions:"
        echo "Please check the test results manually in Synapse Analytics Studio:"
        echo ""
        echo "1. Open Synapse Analytics Studio: https://web.azuresynapse.net/"
        echo "2. Navigate to Data > Databases > logging > Tables > e2e_test_results"
        echo "3. Run this SQL query:"
        echo ""
        echo "   SELECT test_status, entity, test_timestamp"
        echo "   FROM logging.e2e_test_results"
        echo "   WHERE test_timestamp >= DATEADD(hour, -${HOURS_BACK}, GETDATE())"
        echo "   ORDER BY test_timestamp DESC"
        echo ""
        echo "4. Verify that test_status shows 'PASSED' for recent runs"
        exit 1
    fi
    
    echo "No recent test results found. Waiting... (${ELAPSED}s/${MAX_WAIT_SECONDS}s)"
    sleep 30
done
