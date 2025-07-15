**PR Template**

 1. Are there new source to raw datasets?
	
	 - [ ] If yes -has a trigger been attached at the appropriate frequency?
  	 - [ ] If No

 2. Have any new tables been created in Standardised?

  	- [ ] If No
   	- [ ] If yes:
		- [ ] orchestration.json has been updated and tested in Dev and has been / is about to be PRd into main
		- [ ] the new schema exists inside *odw-config/standardised-table-definitions* OR is a about to be PRd into main
			- Make sure to run Platform Integrate and Platform Deploy to Dev at least to ensure the schema is deployed into Synapse Dev Live 
		- [ ] Is the raw-to-standardised python script scheduled to run for this dataset grouping?
 3. Have any new tables been created in Harmonised or Curated?

   	- [ ] If No
	- [ ] If yes:
 		- [ ] *2-odw-standardised-to-harmonised/py_odw_harmonised_table_creation* OR 4-*odw-harmonised-to-curated/py_odw_curated_table_creation
                       are set up to run in the pipeline *pln_post_deployments* with the base parameter specifying the correct table
		- [ ] the new schema exists inside *odw-config/harmonised-table-definitions* / *odw-config/curated-table-definitions* OR is about to be PRd into main
			- Make sure to run Platform Integrate and Platform Deploy to Dev at least to ensure the schema is deployed into Synapse Dev Live 
 4. Have any tables changed AND/OR have any columns changed in any scripts?
    We only care about new columns or columns that change type.
	- [ ] If No
 	- [ ] If yes:
		- [ ] Please set py_change_table to run in the pipeline *pln_post_deployments*
		- [ ] Please create a script to backdate and fill in this new column in Test and Prod
			-Only delete and recreate tables with caution!
 5. Have any scripts run in isolation in dev? Please look at the *"spark.autotune.trackingId"*
	If these changes need to be reflected in Test and Prod, please add to the pipeline *post-deployment/pln_post_deployment*
	- [ ] If yes:
		- [ ] I have reflected this script in the *pln_post_deployments* pipeline
		- [ ] This script is part of a scheduled run and has been added to the appropriate end to end pipeline with a trigger at the correct frequency
	- [ ] If no:
   		- [ ] This change does not need to take place in Test and Prod
	 		- No scripts have run
6. JIRA ticket reference included?
  	- [ ] If yes:
  		- [ ] The correct JIRA ticket is referenced in the PR title and description.
  	- [ ] If no:
		- [ ] Add the correct JIRA ticket reference to the PR title and description before proceeding.
7. Summary of the work provided?
   	- [ ] If yes:
		- [ ] The PR contains a clear summary explaining the purpose and scope of the changes.
  	- [ ] If no:
		- [ ] Write a concise summary of the work in the PR description.
8. Metadata and configuration files updated?
  	- [ ] If yes:
		- [ ] All relevant metadata and configuration files (e.g., pipeline YAML, JSON) have been updated and validated.
  	- [ ] If no:
		- [ ] Update and validate all necessary metadata and configuration files.
9. Pipeline registration completed?
  	- [ ] If yes:
		- [ ] The pipeline is registered in the correct environment and its triggers/parameters are set as intended.
  	- [ ] If no:
		- [ ] Register the pipeline in the target environment and set up triggers/parameters.
10. Table creation and schema validation performed?
  	- [ ] If yes:
		- [ ] Required tables are created and schema has been validated against requirements.
  	- [ ] If no:
		- [ ] Create the necessary tables and validate the schema.
11. Azure Function setup and testing completed?
  	- [ ] If yes:
		- [ ] Azure Functions are deployed and configured.
		- [ ] Unit and integration tests have been run and passed.
		- [ ] Logs have been checked for errors.
  	- [ ] If no:
   		- [ ] Deploy and configure Azure Functions, then run and pass all required tests.
12. Key Vault integration done?
  	- [ ] If yes:
		- [ ] Secrets and configuration values are stored in Azure Key Vault.
		- [ ] The pipeline and Azure Functions retrieve secrets as expected.
  	- [ ] If no:
		- [ ] Store secrets in Azure Key Vault and ensure integration with the pipeline and Azure Functions.
13. Final enablement of the pipeline (App Insights logging checked)?
  	- [ ] If yes:
		- [ ] The pipeline is enabled in the target environment.
		- [ ] Creation and execution logs are visible in Application Insights.
  	- [ ] If no:
		- [ ] Enable the pipeline and verify logs in Application Insights.
14. Deployment and schema change handling documented?
	
  	- [ ] If yes:
		- [ ] Deployment process and rollback steps are documented.
		- [ ] Schema change handling procedures are outlined and tested.
  	- [ ] If no:
		- [ ] Document the deployment process, rollback steps, and schema change handling.
15. Warning reviewed: automatic archiving process?

  	- [ ] If yes:
		- [ ] You have reviewed the automatic archiving logic.
		- [ ] Archiving schedules and retention policies have been checked to avoid accidental data loss.
  	- [ ] If no:
		- [ ] Review the automatic archiving logic, schedules, and retention policies.
16. If there is end to end regression testing has been performed over the existing pipeline?
     - [ ] yes:
     - [ ] no
 
