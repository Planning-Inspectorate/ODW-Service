#!/usr/bin/env python3
"""
Automated E2E Test Results Verification Script

This script connects to Azure Synapse Analytics to query the logging.e2e_test_results 
table and verify that recent E2E tests have passed. If any tests failed or no recent 
results are found, the script exits with a non-zero code to fail the Azure DevOps pipeline.

Usage:
    python verify-e2e-test-results.py --synapse-endpoint <endpoint> --hours-back <hours>

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
import os
import sys
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

try:
    import pyodbc
    from azure.identity import ClientSecretCredential
    from azure.core.exceptions import AzureError
except ImportError as e:
    print(f"ERROR: Missing required Python packages: {e}")
    print("Please install required packages:")
    print("pip install pyodbc azure-identity")
    sys.exit(2)


class SynapseE2EVerifier:
    def __init__(self, synapse_endpoint: str, credential: ClientSecretCredential):
        self.synapse_endpoint = synapse_endpoint
        self.credential = credential
        self.connection_string = None
        
    def _build_connection_string(self) -> str:
        """Build ODBC connection string for Synapse Analytics"""
        # Extract workspace name from endpoint
        workspace_name = self.synapse_endpoint.replace("https://", "").split(".")[0]
        
        return (
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server=tcp:{workspace_name}-ondemand.sql.azuresynapse.net,1433;"
            f"Database=master;"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
    
    def _get_access_token(self) -> str:
        """Get access token for Synapse Analytics"""
        try:
            token = self.credential.get_token("https://database.windows.net/.default")
            return token.token
        except AzureError as e:
            print(f"ERROR: Failed to get access token: {e}")
            raise
    
    def connect(self) -> pyodbc.Connection:
        """Connect to Synapse Analytics using service principal authentication"""
        try:
            connection_string = self._build_connection_string()
            access_token = self._get_access_token()
            
            # Convert access token to bytes for pyodbc
            token_bytes = access_token.encode('utf-16-le')
            
            # Create connection with access token
            connection = pyodbc.connect(
                connection_string,
                attrs_before={1256: token_bytes}  # SQL_COPT_SS_ACCESS_TOKEN
            )
            
            print(f"SUCCESS: Connected to Synapse: {self.synapse_endpoint}")
            return connection
            
        except Exception as e:
            print(f"ERROR: Failed to connect to Synapse: {e}")
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
        query = """
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
        WHERE test_timestamp >= DATEADD(hour, -?, GETDATE())
        ORDER BY test_timestamp DESC
        """
        
        print(f"Looking for E2E test results from the last {hours_back} hours...")
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        while True:
            try:
                with self.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute(query, hours_back)
                    results = cursor.fetchall()
                    
                    if not results:
                        elapsed = time.time() - start_time
                        if elapsed < max_wait_seconds:
                            print(f"No recent test results found. Waiting... ({elapsed:.0f}s/{max_wait_seconds}s)")
                            time.sleep(30)  # Wait 30 seconds before retrying
                            continue
                        else:
                            print(f"ERROR: No E2E test results found in the last {hours_back} hours after waiting {max_wait_minutes} minutes")
                            return False
                    
                    # Process results
                    return self._analyze_results(results)
                    
            except Exception as e:
                print(f"ERROR: Failed to query test results: {e}")
                return False
    
    def _analyze_results(self, results: List[Any]) -> bool:
        """Analyze the test results and determine if all tests passed"""
        print(f"\nFound {len(results)} E2E test result(s):")
        print("=" * 80)
        
        all_passed = True
        entities_tested = set()
        
        for row in results:
            entity = row[0]
            test_status = row[1]
            test_timestamp = row[2]
            std_count = row[3]
            hrm_count = row[4]
            hrm_active_count = row[5]
            cur_count = row[6]
            std_to_hrm_match = row[7]
            hrm_to_cur_match = row[8]
            cur_unique_check = row[9]
            
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
        description="Verify E2E test results in Synapse Analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python verify-e2e-test-results.py --synapse-endpoint https://pins-synw-odw-dev-uks.dev.azuresynapse.net/
    python verify-e2e-test-results.py --synapse-endpoint https://pins-synw-odw-dev-uks.dev.azuresynapse.net/ --hours-back 4 --max-wait 15
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
    
    # Validate environment variables
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET') 
    tenant_id = os.getenv('AZURE_TENANT_ID')
    
    if not all([client_id, client_secret, tenant_id]):
        print("ERROR: Missing required environment variables:")
        print("  - AZURE_CLIENT_ID")
        print("  - AZURE_CLIENT_SECRET") 
        print("  - AZURE_TENANT_ID")
        sys.exit(2)
    
    print("Starting E2E Test Results Verification")
    print(f"Synapse Endpoint: {args.synapse_endpoint}")
    print(f"Looking back: {args.hours_back} hours")
    print(f"Max wait time: {args.max_wait} minutes")
    print("-" * 60)
    
    try:
        # Create credential and verifier
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id, 
            client_secret=client_secret
        )
        
        verifier = SynapseE2EVerifier(args.synapse_endpoint, credential)
        
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
