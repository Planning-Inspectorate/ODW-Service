#!/usr/bin/env python3
"""
Automated E2E Test Results Verification Script (Azure CLI Version)

This script uses Azure CLI to query the logging.e2e_test_results table in Synapse 
Analytics to verify that recent E2E tests have passed. This version avoids ODBC 
dependencies by using Azure CLI for SQL queries.

Usage:
    python verify-e2e-test-results-cli.py --synapse-endpoint <endpoint> --hours-back <hours>

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
import subprocess
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class AzureCLIE2EVerifier:
    def __init__(self, synapse_endpoint: str):
        self.synapse_endpoint = synapse_endpoint
        self.workspace_name = self._extract_workspace_name()
        
    def _extract_workspace_name(self) -> str:
        """Extract workspace name from Synapse endpoint"""
        return self.synapse_endpoint.replace("https://", "").split(".")[0]
    
    def _run_azure_cli_command(self, command: List[str]) -> Dict[str, Any]:
        """Execute an Azure CLI command and return JSON result"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout) if result.stdout.strip() else {}
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Azure CLI command failed: {' '.join(command)}")
            print(f"Error output: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse Azure CLI output as JSON: {e}")
            print(f"Raw output: {result.stdout}")
            raise
    
    def verify_test_results(self, hours_back: int = 2, max_wait_minutes: int = 10) -> bool:
        """
        Query the e2e_test_results table using Azure CLI and verify all recent tests passed
        
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
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while True:
            try:
                # Use Azure CLI to execute SQL query against Synapse serverless pool
                command = [
                    "az", "synapse", "sql", "query",
                    "--workspace-name", self.workspace_name,
                    "--sql-database", "master",
                    "--query-text", query,
                    "--output", "json"
                ]
                
                print(f"Executing query against workspace: {self.workspace_name}")
                result = self._run_azure_cli_command(command)
                
                # The result should be a list of rows
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
        description="Verify E2E test results in Synapse Analytics using Azure CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python verify-e2e-test-results-cli.py --synapse-endpoint https://pins-synw-odw-dev-uks.dev.azuresynapse.net/
    python verify-e2e-test-results-cli.py --synapse-endpoint https://pins-synw-odw-dev-uks.dev.azuresynapse.net/ --hours-back 4 --max-wait 15
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
    
    print("Starting E2E Test Results Verification (Azure CLI Version)")
    print(f"Synapse Endpoint: {args.synapse_endpoint}")
    print(f"Looking back: {args.hours_back} hours")
    print(f"Max wait time: {args.max_wait} minutes")
    print("-" * 60)
    
    try:
        verifier = AzureCLIE2EVerifier(args.synapse_endpoint)
        
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
