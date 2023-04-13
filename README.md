# Introduction
This repo contains all the artifacts and infrastructure code for the PINS Operational Data Warehouse (ODW). It consists of the following:
* [Infrastructure](infrastructure/) - Contains the root Terraform module for deploying the ODW environment
* [Pipelines](pipelines/) - Contains Azure DevOps Pipeline definitions and steps
* [Workspace](workspace/) - Contains development data artifacts ingested into the development Azure Synapse Workspace

# Reference Documentation
* Azure Data Landscape
  * [Azure data management and analytics scenario](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/data-management/)
  * [Analytics end-to-end with Azure Synapse](https://docs.microsoft.com/en-us/azure/architecture/example-scenario/dataplate2e/data-platform-end-to-end?tabs=portal)
  * [Synapse workspaces and lakehouses best practice](https://techcommunity.microsoft.com/t5/azure-synapse-analytics-blog/the-best-practices-for-organizing-synapse-workspaces-and/ba-p/3002506)
* Azure Synapse
  * [Source Control](https://docs.microsoft.com/en-us/azure/synapse-analytics/cicd/source-control)
  * [CI/CD](https://docs.microsoft.com/en-us/azure/synapse-analytics/cicd/continuous-integration-delivery)
  * [Access Control](https://docs.microsoft.com/en-us/azure/synapse-analytics/security/how-to-set-up-access-control)
* Terraform
  * [Data Landing Zone Architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/data-landing-zone#data-landing-zone-architecture)
  * [CI/CD Terraform Deployment with Azure DevOps](https://www.azuredevopslabs.com/labs/vstsextend/terraform/)

# Getting Started
The following steps outline how to get up and running with this repo on your own system:
1.  Environment access
    1.  Github access - if you're reading this repo readme you probably already have this
    2.  Azure DevOps access to the [operational-data-warehouse](https://dev.azure.com/planninginspectorate/operational-data-warehouse) Azure DevOps project
    3.  Azure Portal access - additional access is required to the Azure Portal and the corresponding [Azure Resources in each environment](#environments)
2.  Application Installation - the following desktop applications are optional but provide advantages when working with some of the Azure resources - PINS Azure auth policy is to restrict access to PINS devices only so non-PINS devices will need to be whitelisted to use these
      1. Install [Visual Studio Code](https://code.visualstudio.com/) or equivalent IDE - for editing and commiting code artifacts
      2. Install [Azure Data Studio](https://docs.microsoft.com/en-us/sql/azure-data-studio) - for connecting to Azure SQL instances and managing/commiting data notebooks
      3. Install [Microsoft Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)
3.  Clone Repo
    1. Create a Personal Access Token in GitHub or use another authentication method e.g. SSH
    2. Clone the repo in VSCode/Azure Data Studio to a local folder

# Environments
The ODW environment is deployed to three Azure subscriptions as follows:

| Environment Name | Subscription Name | Subscription ID |
|------------------|-------------------|-----------------|
| Development | pins-odw-data-dev-sub | ff442a29-fc06-4a13-8e3e-65fd5da513b3 |
| Pre-Production | pins-odw-data-preprod-sub | 6b18ba9d-2399-48b5-a834-e0f267be122d |
| Production | pins-odw-data-prod-sub | a82fd28d-5989-4e06-a0bb-1a5d859f9e0c |

Within each subscription, the infrastructure is split into several resource groups, aligned to the [data landing zone architecture](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/architectures/data-landing-zone#data-landing-zone-architecture):

| Resource Group Name | Description |
|---------------------|---------|
| pins-rg-data-odw-_{env}_-_{region}_ | Contains the Data Lake and Synapse Workspace resources |
| pins-rg-data-odw-_{env}_-_{region}_-synapse-managed | Managed resource group for the Synapse Workspace |
| pins-rg-datamgmt-odw-_{env}_-_{region}_ | Contains data management resource such as Purview and Bastion VM(s) |
| pins-rg-datamgmt-odw-_{env}_-_{region}_-purview-managed | Managed resource group for the Purview Account |
| pins-rg-devops-odw-_{env}_-_{region}_ | Contains Azue DevOps agents for deployments into the private network |
| pins-rg-monitoring-odw-_{env}_-_{region}_ | Contains monitoring resources such as Log Analytics and App Insights |
| pins-rg-network-odw-_{env}_-global | Contains private DNS zones for private-link-enabled resources |
| pins-rg-network-odw-_{env}_-_{region}_ | Contains the virtual network, network security groups and private endpoints |
| pins-rg-shir-odw-_{env}_-_{region}_ | Contains self-hosted integration runtime VM(s) used by the Synapse Workspace |

Some of the key resources used in the deployment are:
| Resource Name | Description |
|---------------|-------------|
| Synapse Workspace | Analytics product for loading, transforming and analysing data using SQL and/or Spark |
| ADLS Storage Account | Hierarchical namespace enabled Storage Account to act as a data lake |
| Key Vault | Secrets storage for connection strings, password, etc for connected services |
| Log Analytics | Activity and metric diagnostic log storage with querying capabilities using KQL |


# Processes

## Raw to Standardised Layer 

 The raw layer in the ODW exists as a sink of data from various PINS systems. The standardised layer makes this data available in Delta tables, which are then able to be queried and transformed into a data model in harmonised. The function of Raw to Standardised, then, is simply to take csv and excel files which arrive into the ODW and put them into tables that can be queried and transformed with Spark SQL. We do so by defining the raw sources in our orchestration.json which is a key part of this layer.

### Understanding Orchestration.json

- Head over to `infrastructure/configuration/data-lake/orchestration/orchestration.json`. This file contains an array of definitions where each definition is a raw source. Consider the following definition for an example

```
{
	"Source_ID": 1,
	"Source_Folder": "Fileshare/SAP_HR/HR",
	"Source_Frequency_Folder": "Weekly",
	"Source_Folder_Date_Format": "YYYY-MM-DD",
	"Source_Filename_Format": "Addresses - YYYYMMDD.XLSX",
	"Source_Filename_Start": "Addresses - ",
	"Source_Filename_Date_Format": "YYYYMMDD",
	"Completion_Frequency_CRON": "0 0 * * 1",
	"Expected_Within_Weekdays": 5,
	"Standardised_Path": "HR",
	"Standardised_Table_Name": "hr_addresses",
	"Standardised_Table_Definition": "standardised_table_definitions/addresses.JSON"
}
```

-   **Source_ID** : Unique value for each definition in the array, starting at 1 and increasing in values of 1
-   **Source_Folder**: The folder within [synapse_data_lake]/odw-raw/ that the source file date folders are located. Using the example above, within [synapse_data_lake]/odw-raw/Fileshare/SAP_HR/HR/ we would expect all data pertaining to this Source_ID to sit under this folder.
-   **Source_Frequency_Folder**: If the data is to be received at multiple frequencies, the next folder underneath Source_Folder in the folder structure should be ‘Weekly’ or ‘Monthly’
-   **Source_Folder_Date_Format**: This is the format of the last folder in the folder structure within which our file sits. For the above example, this might be [synapse_data_lake]/odw-raw/Fileshare/SAP_HR/HR/Weekly/2022-10-01/
-   **Source_Filename_Format**: This entry describes the format of the name of the source file
-   **Source_Filename_Start**: This string should be contained within our filename and uniquely identify a single file within our example folder structure above. So, for ‘Addresses - 20221001.XLSX’, ‘Addresses - ‘ would be able to uniquely identify the file. Only one file with this naming should be available in the dated folder.
-   **Source_Filename_Date_Format**: The format of the date in the filename. ‘None’ if none in use.
-   **Completion_Frequency_CRON**: This CRON notation determines the frequency at which we would expect a file for this Source_ID to arrive. Use [crontab guru](https://crontab.guru/) to translate into plaintext what each CRON means.
-   **Expected_Within_Weekdays**: The Completion_Frequency_CRON parameter can determine when the last expected date for the file was, but to determine when we expect the file by, we add the number of days on according to this parameter.
-   **Standardised_Path**: This is the path to the standardised Delta table storage folder in the synapse data lake storage within [synapse_data_lake]/odw-standardised/
-   **Standardised_Table_Name**: This is the name of the standardised Delta table
-   **Standardised_Table_Definition**: This is the location of the Json schema for the standardised Delta table, and will be located within [synapse_data_lake]/odw-config/standardised_table_definitions

### Adding a new Raw Source

In order to add a new raw source and convert the data in standardised form, follow the following steps

- Create a new branch and add a new record in the `orchestration.json` file. This new record will have a new `Source_ID` which we will use at a later step.
- Generate a PR of your branch and after it gets merged, head over to the [Azure DevOps](https://dev.azure.com/planninginspectorate/operational-data-warehouse/_build) and run the **Platform Deploy** pipeline. This will deploy your changes into Synapse.
- When the pipeline succeeds, go to `[synapse_data_lake]/odw-config/orchestration/orchestration.json` and verify that your change has been deployed.
- Go to the pipeline `pln_raw_to_standardised_e2e` and set the new `Source_ID` in the first activity of the pipeline called "Set SourceID".
	- Click the activity Set SourceID > Settings > Edit the Value of the variable
- Run the pipeline and cross your fingers. If it succeeds, you should be able to find your Standardised table at the specified location with the data ingested.
