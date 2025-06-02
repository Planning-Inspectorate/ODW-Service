module "synapse_workspace_private" {
  source = "./modules/synapse-workspace-private"

  environment         = var.environment
  resource_group_name = azurerm_resource_group.data.name
  location            = module.azure_region.location_cli
  service_name        = local.service_name

  data_lake_account_id                  = module.synapse_data_lake.data_lake_account_id
  data_lake_account_id_failover         = module.synapse_data_lake_failover.data_lake_account_id
  data_lake_account_name                = module.synapse_data_lake.data_lake_account_name
  data_lake_account_name_failover       = module.synapse_data_lake_failover.data_lake_account_name
  data_lake_filesystem_id               = module.synapse_data_lake.data_lake_filesystem_id
  firewall_allowed_ip_addresses         = local.firewall_allowed_ip_addresses
  key_vault_id                          = module.synapse_data_lake.key_vault_id
  key_vault_name                        = module.synapse_data_lake.key_vault_name
  network_resource_group_name           = azurerm_resource_group.network.name
  purview_ids                           = var.create_purview_account ? module.synapse_management.purview_ids : null
  spark_pool_enabled                    = var.spark_pool_enabled
  spark_pool_max_node_count             = var.spark_pool_max_node_count
  spark_pool_min_node_count             = var.spark_pool_min_node_count
  spark_pool_node_size                  = var.spark_pool_node_size
  spark_pool_preview_enabled            = var.spark_pool_preview_enabled
  spark_pool_preview_requirements       = file("${path.module}/configuration/spark-pool/requirements-preview.txt")
  spark_pool_preview_version            = var.spark_pool_preview_version
  spark_pool_requirements               = file("${path.module}/configuration/spark-pool/requirements.txt")
  spark_pool_timeout_minutes            = var.spark_pool_timeout_minutes
  spark_pool_version                    = var.spark_pool_version
  new_spark_pool_version                = var.new_spark_pool_version
  sql_pool_enabled                      = var.sql_pool_enabled
  sql_pool_collation                    = var.sql_pool_collation
  sql_pool_sku_name                     = var.sql_pool_sku_name
  synapse_aad_administrator             = var.synapse_aad_administrator
  synapse_data_exfiltration_enabled     = var.synapse_data_exfiltration_enabled
  synapse_private_endpoint_dns_zone_id  = azurerm_private_dns_zone.synapse.id
  synapse_private_endpoint_subnet_name  = local.synapse_subnet_name
  synapse_private_endpoint_vnet_subnets = module.synapse_network.vnet_subnets
  synapse_sql_administrator_username    = var.synapse_sql_administrator_username
  synapse_role_assignments              = var.synapse_role_assignments
  tenant_id                             = var.tenant_id
  tooling_config = {
    synapse_private_dns_zone_id     = data.azurerm_private_dns_zone.tooling_synapse.id
    synapse_dev_private_dns_zone_id = data.azurerm_private_dns_zone.tooling_synapse_dev.id
  }

  create_service_bus_resources           = true
  odt_appeals_back_office_service_bus_id = var.odt_appeals_back_office.service_bus_enabled && var.external_resource_links_enabled ? data.azurerm_servicebus_namespace.odt_appeals_backoffice_sb[0].id : null

  tags = local.tags

  providers = {
    azurerm     = azurerm,
    azurerm.odt = azurerm.odt
  }
}

module "synapse_workspace_private_failover" {
  count = var.failover_deployment ? 1 : 0

  source = "./modules/synapse-workspace-private"

  environment         = var.environment
  resource_group_name = azurerm_resource_group.data_failover.name
  location            = module.azure_region.paired_location.location_cli
  service_name        = local.service_name

  data_lake_account_id                  = module.synapse_data_lake_failover.data_lake_account_id
  data_lake_account_id_failover         = module.synapse_data_lake.data_lake_account_id
  data_lake_account_name                = module.synapse_data_lake_failover.data_lake_account_name
  data_lake_account_name_failover       = module.synapse_data_lake.data_lake_account_name
  data_lake_filesystem_id               = module.synapse_data_lake_failover.data_lake_filesystem_id
  firewall_allowed_ip_addresses         = local.firewall_allowed_ip_addresses
  key_vault_id                          = module.synapse_data_lake_failover.key_vault_id
  key_vault_name                        = module.synapse_data_lake_failover.key_vault_name
  network_resource_group_name           = azurerm_resource_group.network_failover.name
  purview_ids                           = var.create_purview_account ? module.synapse_management_failover.purview_ids : null
  spark_pool_enabled                    = var.spark_pool_enabled
  spark_pool_max_node_count             = var.spark_pool_max_node_count
  spark_pool_min_node_count             = var.spark_pool_min_node_count
  spark_pool_node_size                  = var.spark_pool_node_size
  spark_pool_preview_enabled            = var.spark_pool_preview_enabled
  spark_pool_preview_requirements       = file("${path.module}/configuration/spark-pool/requirements-preview.txt")
  spark_pool_preview_version            = var.spark_pool_preview_version
  spark_pool_requirements               = file("${path.module}/configuration/spark-pool/requirements.txt")
  spark_pool_timeout_minutes            = var.spark_pool_timeout_minutes
  spark_pool_version                    = var.spark_pool_version
  new_spark_pool_version                = var.new_spark_pool_version
  sql_pool_enabled                      = var.sql_pool_enabled
  sql_pool_collation                    = var.sql_pool_collation
  sql_pool_sku_name                     = var.sql_pool_sku_name
  synapse_aad_administrator             = var.synapse_aad_administrator
  synapse_data_exfiltration_enabled     = var.synapse_data_exfiltration_enabled
  synapse_private_endpoint_dns_zone_id  = azurerm_private_dns_zone.synapse.id
  synapse_private_endpoint_subnet_name  = local.synapse_subnet_name
  synapse_private_endpoint_vnet_subnets = module.synapse_network_failover.vnet_subnets
  synapse_sql_administrator_username    = var.synapse_sql_administrator_username
  synapse_role_assignments              = var.synapse_role_assignments
  tenant_id                             = var.tenant_id
  tooling_config = {
    synapse_private_dns_zone_id     = data.azurerm_private_dns_zone.tooling_synapse.id
    synapse_dev_private_dns_zone_id = data.azurerm_private_dns_zone.tooling_synapse_dev.id
  }

  tags = local.tags

  providers = {
    azurerm     = azurerm,
    azurerm.odt = azurerm.odt
  }
}
