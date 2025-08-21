from tests.util.pipeline_run_test_case import PipelineRunTestCase
import pytest


class TestE2EPlnMasterTest(PipelineRunTestCase):
    def test_pln_master_test_pipeline(self):
        """
        Test the pln_master_test pipeline which runs E2E data validation
        across all enabled entities in the system.
        """
        pipeline_result = self.run_pipeline(
            "pln_master_test",
            {},  # No parameters needed - pipeline gets entities from orchestration config
            max_wait_time_minutes=60  # Extended timeout for comprehensive E2E testing
        )
        
        # The pipeline should complete successfully
        assert pipeline_result["status"] == "Succeeded"
