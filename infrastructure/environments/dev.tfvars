alert_group_platform_enabled             = false
alert_group_platform_recipients          = ["lester.march@planninginspectorate.gov.uk"]
alert_group_synapse_enabled              = false
alert_group_synapse_recipients           = ["lester.march@planninginspectorate.gov.uk"]
alert_scope_service_health               = "/subscriptions/ff442a29-fc06-4a13-8e3e-65fd5da513b3"
alert_threshold_data_lake_capacity_bytes = 10995116277760 # 10TiB

bastion_host_enabled = true
bastion_vm_username  = "basadmin"
bastion_vm_size      = "Standard_F2s_v2"
bastion_vm_image = {
  publisher = "microsoft-dsvm"
  offer     = "dsvm-win-2019"
  sku       = "winserver-2019"
  version   = "latest"
}

data_lake_account_tier     = "Standard"
data_lake_replication_type = "GRS"
data_lake_retention_days   = 7
data_lake_role_assignments = {
  "Storage Blob Data Contributor" = [
    "ebcc4498-4abe-4457-8970-7fa08bf87543", # pins-odw-dev-administrators
    "48bd5755-6d7d-4a17-b044-7522c54e9c7d", # pins-odw-dev-dataengineers
    "b4dbfba4-b78b-4163-9b39-87ea03e2d5ed"  # planninginspectorate-operational-data-warehouse-ff442a29-fc06-4a13-8e3e-65fd5da513b3
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

devops_agent_pool_resource_group_name          = "pins-rg-devops-odw-dev-uks"
devops_agent_pool_resource_group_name_failover = "pins-rg-devops-odw-dev-ukw"

firewall_allowed_ip_addresses = [
  "2.218.104.16",    # K+C Michael
  "77.108.155.244",  # K+C Manchester Office 1
  "77.108.155.245",  # K+C Manchester Office 2
  "81.144.234.220",  # K+C London Office 1
  "81.144.234.221",  # K+C London Office 2
  "82.28.123.122",   # K+C Maria
  "86.31.135.222",   # PINS Bristol Office 1
  "86.166.41.93",    # K+C Daya
  "109.153.205.252", # K+C Lester
  "212.58.61.170",   # K+C London Office 3
  "213.78.68.18"     # K+C London Office 4
]

environment = "dev"
location    = "uk-south"

key_vault_role_assignments = {
  "Key Vault Administrator" = [
    "ebcc4498-4abe-4457-8970-7fa08bf87543" # pins-odw-dev-administrators
  ],
  "Key Vault Secrets Officer" = [
    "48bd5755-6d7d-4a17-b044-7522c54e9c7d" # pins-odw-dev-dataengineers
  ]
}

network_watcher_enabled = false

spark_pool_enabled        = true
spark_pool_max_node_count = 12
spark_pool_min_node_count = 3
spark_pool_node_size      = "Small"
spark_pool_version        = "3.2"

sql_pool_collation = "SQL_Latin1_General_CP1_CI_AS"
sql_pool_enabled   = true
sql_pool_sku_name  = "DW100c"

sql_server_administrator_username = "sqladmin"
sql_server_enabled                = true

synapse_aad_administrator = {
  username  = "pins-odw-data-dev-syn-ws-sqladmins"
  object_id = "1c996957-30e4-40fe-b0b4-82d40f13c058"
}

synapse_data_exfiltration_enabled  = false
synapse_sql_administrator_username = "synadmin"
synapse_role_assignments = {
  "Synapse Administrator" = [
    "6a38f212-3834-4e2e-93fb-f81bb3a3fe49", # pins-odw-data-dev-syn-ws-administrators
    "b4dbfba4-b78b-4163-9b39-87ea03e2d5ed"  # planninginspectorate-operational-data-warehouse-ff442a29-fc06-4a13-8e3e-65fd5da513b3
  ],
  "Synapse Contributor" = [
    "0a5073e3-b8e9-4786-8e1f-39f2c277aeb2" # pins-odw-data-dev-syn-ws-contributors
  ],
  "Synapse Compute Operator" = [
    "a66ee73a-c31b-451d-b13e-19b4e92c0c25" # pins-odw-data-dev-syn-ws-computeoperators
  ]
}

tags = {}

tenant_id = "5878df98-6f88-48ab-9322-998ce557088d"

vnet_base_cidr_block          = "10.70.0.0/24"
vnet_base_cidr_block_failover = "10.70.1.0/24"
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
