#!/usr/bin/env python3
"""
Automated E2E Test Results Verification Script (REST API Version)

This script uses REST API calls to query the logging.e2e_test_results table in Synapse 
Analytics to verify that recent E2E tests have passed. This version uses direct REST API 
calls instead of Azure CLI to avoid command compatibility issues.

Usage:
    python verify-e2e-test-results-rest.py --synapse-endpoint <endpoint> --hours-back <hours>

Environment Variables Required:
    - AZURE_CLIENT_ID: Service Principal Client ID
    - AZURE_CLIENT_SECRET: Service Principal Secret  
    - AZURE_TENANT_ID: Azure Tenant ID

Exit Codes:
    0: All tests passed
    1: Test failures found or no recent results
    2: Connection or query error
"""

import argparse
import json
import os
import requests
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class RestAPIE2EVerifier:
    def __init__(self, synapse_endpoint: str):
        self.synapse_endpoint = synapse_endpoint
        self.workspace_name = self._extract_workspace_name()
        self.access_token = None
        
    def _extract_workspace_name(self) -> str:
        """Extract workspace name from Synapse endpoint"""
        return self.synapse_endpoint.replace("https://", "").split(".")[0]
    
    def _get_access_token(self) -> str:
        """Get access token using service principal credentials"""
        if self.access_token:
            return self.access_token
            
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        tenant_id = os.getenv('AZURE_TENANT_ID')
        
        if not all([client_id, client_secret, tenant_id]):
            raise Exception("Missing required environment variables: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID")
        
        # Get access token from Azure AD
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://dev.azuresynapse.net/.default'
        }
        
        try:
            response = requests.post(token_url, data=token_data)
            response.raise_for_status()
            token_response = response.json()
            self.access_token = token_response['access_token']
            print("Successfully obtained access token")
            return self.access_token
        except Exception as e:
            print(f"ERROR: Failed to get access token: {e}")
            raise
    
    def _execute_sql_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query against Synapse serverless SQL pool"""
        access_token = self._get_access_token()
        
        # Use the serverless SQL endpoint
        sql_endpoint = f"https://{self.workspace_name}-ondemand.sql.azuresynapse.net"
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Use the SQL query endpoint
        query_url = f"{sql_endpoint}/sql/query"
        
        query_payload = {
            'query': query,
            'database': 'master'
        }
        
        try:
            response = requests.post(query_url, headers=headers, json=query_payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: SQL query failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            raise
    
    def verify_test_results(self, hours_back: int = 2, max_wait_minutes: int = 10) -> bool:
        """
        Query the e2e_test_results table and verify all recent tests passed
        
        Args:
            hours_back: How many hours back to look for test results
            max_wait_minutes: Maximum time to wait for test results
            
        Returns:
            bool: True if all tests passed, False otherwise
        """
        query = f"""
        SELECT 
            entity,
            test_status,
            test_timestamp,
            std_count,
            hrm_count,
            hrm_active_count,
            cur_count,
            std_to_hrm_match,
            hrm_to_cur_match,
            cur_unique_check
        FROM logging.e2e_test_results 
        WHERE test_timestamp >= DATEADD(hour, -{hours_back}, GETDATE())
        ORDER BY test_timestamp DESC
        """
        
        print(f"Looking for E2E test results from the last {hours_back} hours...")
        print(f"Workspace: {self.workspace_name}")
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while True:
            try:
                print("Executing SQL query against Synapse serverless pool...")
                result = self._execute_sql_query(query)
                
                # Check if we have results
                if not result or len(result) == 0:
                    elapsed = time.time() - start_time
                    if elapsed < max_wait_seconds:
                        print(f"No recent test results found. Waiting... ({elapsed:.0f}s/{max_wait_seconds}s)")
                        time.sleep(30)  # Wait 30 seconds before retrying
                        continue
                    else:
                        print(f"ERROR: No E2E test results found in the last {hours_back} hours after waiting {max_wait_minutes} minutes")
                        return False
                
                # Process results
                return self._analyze_results(result)
                
            except Exception as e:
                print(f"ERROR: Failed to query test results: {e}")
                return False
    
    def _analyze_results(self, results: List[Dict[str, Any]]) -> bool:
        """Analyze the test results and determine if all tests passed"""
        print(f"\nFound {len(results)} E2E test result(s):")
        print("=" * 80)
        
        all_passed = True
        entities_tested = set()
        
        for row in results:
            entity = row.get('entity', 'Unknown')
            test_status = row.get('test_status', 'Unknown')
            test_timestamp = row.get('test_timestamp', 'Unknown')
            std_count = row.get('std_count', 0)
            hrm_count = row.get('hrm_count', 0)
            hrm_active_count = row.get('hrm_active_count', 0)
            cur_count = row.get('cur_count', 0)
            std_to_hrm_match = row.get('std_to_hrm_match', False)
            hrm_to_cur_match = row.get('hrm_to_cur_match', False)
            cur_unique_check = row.get('cur_unique_check', False)
            
            entities_tested.add(entity)
            
            status_indicator = "PASS" if test_status == "PASSED" else "FAIL"
            print(f"[{status_indicator}] Entity: {entity}")
            print(f"   Status: {test_status}")
            print(f"   Timestamp: {test_timestamp}")
            print(f"   Counts: STD={std_count}, HRM={hrm_count}, HRM_Active={hrm_active_count}, CUR={cur_count}")
            print(f"   Validations: STD->HRM={std_to_hrm_match}, HRM->CUR={hrm_to_cur_match}, Unique={cur_unique_check}")
            
            if test_status != "PASSED":
                all_passed = False
                print(f"   FAILURE DETAILS: {test_status}")
            
            print("-" * 40)
        
        print(f"\nSUMMARY:")
        print(f"   Entities tested: {len(entities_tested)}")
        print(f"   Total test records: {len(results)}")
        print(f"   Entities: {', '.join(sorted(entities_tested))}")
        
        if all_passed:
            print("SUCCESS: All E2E tests PASSED!")
            return True
        else:
            print("FAILURE: One or more E2E tests FAILED!")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify E2E test results in Synapse Analytics using REST API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python verify-e2e-test-results-rest.py --synapse-endpoint https://pins-synw-odw-dev-uks.dev.azuresynapse.net/
    python verify-e2e-test-results-rest.py --synapse-endpoint https://pins-synw-odw-dev-uks.dev.azuresynapse.net/ --hours-back 4 --max-wait 15
        """
    )
    
    parser.add_argument(
        '--synapse-endpoint',
        required=True,
        help='Synapse Analytics workspace endpoint URL'
    )
    
    parser.add_argument(
        '--hours-back',
        type=int,
        default=2,
        help='How many hours back to look for test results (default: 2)'
    )
    
    parser.add_argument(
        '--max-wait',
        type=int,
        default=10,
        help='Maximum minutes to wait for test results (default: 10)'
    )
    
    args = parser.parse_args()
    
    print("Starting E2E Test Results Verification (REST API Version)")
    print(f"Synapse Endpoint: {args.synapse_endpoint}")
    print(f"Looking back: {args.hours_back} hours")
    print(f"Max wait time: {args.max_wait} minutes")
    print("-" * 60)
    
    try:
        verifier = RestAPIE2EVerifier(args.synapse_endpoint)
        
        # Verify test results
        success = verifier.verify_test_results(
            hours_back=args.hours_back,
            max_wait_minutes=args.max_wait
        )
        
        if success:
            print("\nE2E Test Verification: PASSED")
            sys.exit(0)
        else:
            print("\nE2E Test Verification: FAILED")
            print("\nThe Azure DevOps pipeline will now fail to prevent false positive results.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nVerification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during verification: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
