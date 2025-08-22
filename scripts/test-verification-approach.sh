#!/bin/bash

# Test script to validate the E2E verification approach
# This script tests the verification logic without connecting to actual Synapse

echo "Testing E2E Verification Approach"
echo "=================================="

# Test 1: Basic script validation
echo "Test 1: Basic script validation..."
if bash -n verify-e2e-test-results.sh; then
    echo "✓ Script syntax is valid"
else
    echo "✗ Script has syntax errors"
    exit 1
fi

# Test 2: Parameter validation
echo -e "\nTest 2: Parameter validation..."
output=$(bash verify-e2e-test-results.sh 2>&1 || true)
if echo "$output" | grep -q "ERROR: Workspace name is required"; then
    echo "✓ Parameter validation works correctly"
else
    echo "✗ Parameter validation failed"
    echo "Output: $output"
    exit 1
fi

# Test 3: Azure CLI availability
echo -e "\nTest 3: Azure CLI availability..."
if command -v az >/dev/null 2>&1; then
    echo "✓ Azure CLI is available"
    
    # Test Azure CLI access token command (will fail without login, but command structure is valid)
    if az account get-access-token --help >/dev/null 2>&1; then
        echo "✓ Azure CLI get-access-token command is available"
    else
        echo "✗ Azure CLI get-access-token command not available"
        exit 1
    fi
else
    echo "✗ Azure CLI not found"
    exit 1
fi

# Test 4: curl availability
echo -e "\nTest 4: curl availability..."
if command -v curl >/dev/null 2>&1; then
    echo "✓ curl is available"
else
    echo "✗ curl not found"
    exit 1
fi

# Test 5: Python JSON parsing
echo -e "\nTest 5: Python JSON parsing capability..."
test_json='{"entity": "test-entity", "test_status": "PASSED"}'
result=$(echo "$test_json" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"Entity: {data['entity']}, Status: {data['test_status']}\")
    sys.exit(0)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✓ Python JSON parsing works"
    echo "  Result: $result"
else
    echo "✗ Python JSON parsing failed"
    exit 1
fi

# Test 6: Mock API response processing
echo -e "\nTest 6: Mock API response processing..."
mock_response='[{"entity": "appeal-has", "test_status": "PASSED", "test_timestamp": "2024-01-01T10:00:00"}, {"entity": "appeal-outcome", "test_status": "PASSED", "test_timestamp": "2024-01-01T10:01:00"}]'

result=$(echo "$mock_response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    all_passed = True
    entities_tested = set()
    
    for row in data:
        entity = row.get('entity', 'Unknown')
        test_status = row.get('test_status', 'Unknown')
        entities_tested.add(entity)
        
        status_indicator = 'PASS' if test_status == 'PASSED' else 'FAIL'
        print(f'[{status_indicator}] Entity: {entity}, Status: {test_status}')
        
        if test_status != 'PASSED':
            all_passed = False
    
    print(f'Summary: {len(entities_tested)} entities tested')
    print(f'Entities: {\", \".join(sorted(entities_tested))}')
    
    if all_passed:
        print('SUCCESS: All tests PASSED!')
        sys.exit(0)
    else:
        print('FAILURE: Some tests FAILED!')
        sys.exit(1)
        
except Exception as e:
    print(f'Error parsing results: {e}')
    sys.exit(1)
" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✓ Mock API response processing works"
    echo "$result"
else
    echo "✗ Mock API response processing failed"
    exit 1
fi

echo -e "\n✓ All tests passed! The verification approach should work."
echo ""
echo "Next steps to test with real Synapse connection:"
echo "1. Ensure you're logged into Azure CLI: az login"
echo "2. Test with a real workspace: ./verify-e2e-test-results.sh pins-synw-odw-dev-uks 2 1"
echo "3. Check the Azure DevOps pipeline logs for actual execution"
