from tests.util.pipeline_run_test_case import PipelineRunTestCase
import pytest


class TestE2EPlnMasterTest(PipelineRunTestCase):
    def test_pln_master_test_pipeline(self):
        """
        Test the pln_master_test pipeline which runs E2E data validation
        across all enabled entities in the system.
        """
        # Trigger the pipeline
        pipeline_run_id = self._trigger_pipeline(
            "pln_master_test",
            {}  # No parameters needed - pipeline gets entities from orchestration config
        )
        
        # Wait for the pipeline to complete with extended timeout for comprehensive E2E testing
        pipeline_result = self._wait_for_pipeline_run(
            pipeline_run_id,
            max_wait_time_minutes=60
        )
        
        # The pipeline should complete successfully
        assert pipeline_result["status"] == "Succeeded"
