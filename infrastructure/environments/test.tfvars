alert_group_platform_enabled             = true
alert_group_platform_recipients          = ["nasir.rahman@planninginspectorate.gov.uk"]
alert_group_synapse_enabled              = true
alert_group_synapse_recipients           = ["abdullah.pakwashee@planninginspectorate.gov.uk", "alex.delany@planninginspectorate.gov.uk"]
alert_scope_service_health               = "/subscriptions/6b18ba9d-2399-48b5-a834-e0f267be122d"
alert_threshold_data_lake_capacity_bytes = 10995116277760 # 10TiB

bastion_host_enabled = false
bastion_vm_username  = "basadmin"
bastion_vm_size      = "Standard_F2s_v2"
bastion_vm_image = {
  publisher = "microsoft-dsvm"
  offer     = "dsvm-win-2019"
  sku       = "winserver-2019"
  version   = "latest"
}

data_lake_account_tier          = "Standard"
data_lake_config_container_name = "odw-config"
data_lake_replication_type      = "GRS"
data_lake_retention_days        = 7
data_lake_role_assignments = {
  "Storage Blob Data Contributor" = [
    "8274feca-09ef-41b1-9b4e-5eedc3384df4", # pins-odw-preprod-administrators
    "7c906e1b-ffbb-44d3-89a1-6772b9c9c148", # pins-odw-preprod-dataengineers
    "51432f9e-c5a2-468f-8421-5984d097d1f9"  # planninginspectorate-operational-data-warehouse-6b18ba9d-2399-48b5-a834-e0f267be122d
  ]
}
data_lake_storage_containers = [
  "backup-logs",
  "odw-curated",
  "odw-raw",
  "odw-standardised",
  "odw-harmonised",
  "odw-config"
]

devops_agent_pool_resource_group_name          = "pins-rg-devops-odw-test-uks"
devops_agent_pool_resource_group_name_failover = "pins-rg-devops-odw-test-ukw"

environment = "test"
location    = "uk-south"

key_vault_role_assignments = {
  "Key Vault Administrator" = [
    "8274feca-09ef-41b1-9b4e-5eedc3384df4" # pins-odw-preprod-administrators
  ],
  "Key Vault Secrets Officer" = [
    "7c906e1b-ffbb-44d3-89a1-6772b9c9c148" # pins-odw-preprod-dataengineers
  ]
}

network_watcher_enabled = false

odt_back_office_service_bus_enabled                      = true
odt_back_office_service_bus_failover_enabled             = false
odt_back_office_service_bus_name                         = "pins-sb-back-office-test-ukw-001"
odt_back_office_service_bus_name_failover                = "pins-sb-back-office-test-uks-001"
odt_back_office_service_bus_resource_group_name          = "pins-rg-back-office-test-ukw-001"
odt_back_office_service_bus_resource_group_name_failover = "pins-rg-back-office-test-uks-001"
odt_back_office_subscription_id                          = "76cf28c6-6fda-42f1-bcd9-6d7dbed704ef"

service_bus_failover_enabled = false
service_bus_role_assignments = {
  "Azure Service Bus Data Owner" = [
    "8274feca-09ef-41b1-9b4e-5eedc3384df4" # pins-odw-preprod-administrators
  ]
}

service_bus_topics_and_subscriptions = {
  "employee" = [
    "employee",
    "employee-verify"
  ]
}

spark_pool_enabled         = true
spark_pool_max_node_count  = 12
spark_pool_min_node_count  = 3
spark_pool_node_size       = "Small"
spark_pool_timeout_minutes = 15
spark_pool_version         = "3.3"

spark_pool_preview_enabled = true
spark_pool_preview_version = "3.3"

sql_pool_collation = "SQL_Latin1_General_CP1_CI_AS"
sql_pool_enabled   = false
sql_pool_sku_name  = "DW100c"

sql_server_administrator_username = "sqladmin"
sql_server_enabled                = false

synapse_aad_administrator = {
  username  = "pins-odw-data-preprod-syn-ws-sqladmins"
  object_id = "ba5af92f-a1bf-4332-a3c9-613a0a8f1b12"
}

synapse_data_exfiltration_enabled  = false
synapse_sql_administrator_username = "synadmin"
synapse_role_assignments = {
  "Synapse Administrator" = [
    "be52cb0c-858f-4698-8c40-3a5ec793a2e3", # pins-odw-data-preprod-syn-ws-administrators
    "51432f9e-c5a2-468f-8421-5984d097d1f9"  # planninginspectorate-operational-data-warehouse-6b18ba9d-2399-48b5-a834-e0f267be122d
  ],
  "Synapse Contributor" = [
    "d59a3e85-58db-4b70-8f88-3f4a4a82ee27" # pins-odw-data-preprod-syn-ws-contributors
  ],
  "Synapse Compute Operator" = [
    "f9c580cd-cab0-4c49-9f50-290194ade29e" # pins-odw-data-preprod-syn-ws-computeoperators
  ]
}

tags = {}

tenant_id = "5878df98-6f88-48ab-9322-998ce557088d"

vnet_base_cidr_block          = "10.80.0.0/24"
vnet_base_cidr_block_failover = "10.80.1.0/24"
vnet_subnets = [
  {
    "name" : "AzureBastionSubnet",
    "new_bits" : 2 # /26
  },
  {
    "name" : "SynapseEndpointSubnet",
    "new_bits" : 2 # /26
  },
  {
    "name" : "ComputeSubnet"
    "new_bits" : 2 # /26
  },
  {
    "name" : null, # Reserved
    "new_bits" : 2 # /26
  }
]
