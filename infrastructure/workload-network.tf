resource "azurerm_resource_group" "network" {
  name     = "pins-rg-network-${local.resource_suffix}"
  location = module.azure_region.location_cli

  tags = local.tags
}

resource "azurerm_resource_group" "network_failover" {
  name     = "pins-rg-network-${local.resource_suffix_failover}"
  location = module.azure_region.paired_location.location_cli

  tags = local.tags
}

resource "azurerm_resource_group" "network_global" {
  name     = "pins-rg-network-${local.resource_suffix_global}"
  location = module.azure_region.location_cli

  tags = local.tags
}

module "synapse_network" {
  source = "./modules/synapse-network"

  environment         = var.environment
  resource_group_id   = azurerm_resource_group.network.id
  resource_group_name = azurerm_resource_group.network.name
  location            = module.azure_region.location_cli
  service_name        = local.service_name

  network_watcher_enabled = var.network_watcher_enabled
  vnet_base_cidr_block    = var.vnet_base_cidr_block
  vnet_subnets            = var.vnet_subnets

  tags = local.tags
}

module "synapse_network_failover" {
  source = "./modules/synapse-network"

  environment         = var.environment
  resource_group_id   = azurerm_resource_group.network_failover.id
  resource_group_name = azurerm_resource_group.network_failover.name
  location            = module.azure_region.paired_location.location_cli
  service_name        = local.service_name

  network_watcher_enabled = var.network_watcher_enabled
  vnet_base_cidr_block    = var.vnet_base_cidr_block_failover
  vnet_subnets            = var.vnet_subnets

  tags = local.tags
}

resource "azurerm_private_dns_zone" "data_lake" {
  name                = "privatelink.dfs.core.windows.net"
  resource_group_name = azurerm_resource_group.network_global.name

  tags = local.tags
}

resource "azurerm_private_dns_zone" "key_vault" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.network_global.name

  tags = local.tags
}

resource "azurerm_private_dns_zone" "synapse" {
  name                = "privatelink.azuresynapse.net"
  resource_group_name = azurerm_resource_group.network_global.name

  tags = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "data_lake" {
  name                  = "dfs-${module.synapse_network.vnet_name}"
  resource_group_name   = azurerm_resource_group.network_global.name
  private_dns_zone_name = azurerm_private_dns_zone.data_lake.name
  virtual_network_id    = module.synapse_network.vnet_id

  tags = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "data_lake_failover" {
  name                  = "dfs-${module.synapse_network_failover.vnet_name}"
  resource_group_name   = azurerm_resource_group.network_global.name
  private_dns_zone_name = azurerm_private_dns_zone.data_lake.name
  virtual_network_id    = module.synapse_network_failover.vnet_id

  tags = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "key_vault" {
  name                  = "dfs-${module.synapse_network.vnet_name}"
  resource_group_name   = azurerm_resource_group.network_global.name
  private_dns_zone_name = azurerm_private_dns_zone.key_vault.name
  virtual_network_id    = module.synapse_network.vnet_id

  tags = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "key_vault_failover" {
  name                  = "dfs-${module.synapse_network_failover.vnet_name}"
  resource_group_name   = azurerm_resource_group.network_global.name
  private_dns_zone_name = azurerm_private_dns_zone.key_vault.name
  virtual_network_id    = module.synapse_network_failover.vnet_id

  tags = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "synapse" {
  name                  = "azuresynapse-${module.synapse_network.vnet_name}"
  resource_group_name   = azurerm_resource_group.network_global.name
  private_dns_zone_name = azurerm_private_dns_zone.synapse.name
  virtual_network_id    = module.synapse_network.vnet_id

  tags = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "synapse_failover" {
  name                  = "azuresynapse-${module.synapse_network_failover.vnet_name}"
  resource_group_name   = azurerm_resource_group.network_global.name
  private_dns_zone_name = azurerm_private_dns_zone.synapse.name
  virtual_network_id    = module.synapse_network_failover.vnet_id

  tags = local.tags
}

resource "azurerm_virtual_network_peering" "pri_sec" {
  name                      = "peer-${module.synapse_network.vnet_name}-${module.synapse_network_failover.vnet_name}"
  resource_group_name       = azurerm_resource_group.network.name
  virtual_network_name      = module.synapse_network.vnet_name
  remote_virtual_network_id = module.synapse_network_failover.vnet_id
}

resource "azurerm_virtual_network_peering" "sec_pri" {
  name                      = "peer-${module.synapse_network_failover.vnet_name}-${module.synapse_network.vnet_name}"
  resource_group_name       = azurerm_resource_group.network_failover.name
  virtual_network_name      = module.synapse_network_failover.vnet_name
  remote_virtual_network_id = module.synapse_network.vnet_id
}

# peering to tooling VNET

data "azurerm_virtual_network" "tooling" {
  name                = var.tooling_config.network_name
  resource_group_name = var.tooling_config.network_rg

  provider = azurerm.tooling
}

resource "azurerm_virtual_network_peering" "odw_to_tooling" {
  name                      = "pins-peer-${local.service_name}-to-tooling-${var.environment}"
  resource_group_name       = azurerm_resource_group.network.name
  virtual_network_name      = module.synapse_network.vnet_name
  remote_virtual_network_id = data.azurerm_virtual_network.tooling.id
}

resource "azurerm_virtual_network_peering" "tooling_to_odw" {
  name                      = "pins-peer-tooling-to-${local.service_name}-${var.environment}"
  resource_group_name       = var.tooling_config.network_rg
  virtual_network_name      = var.tooling_config.network_name
  remote_virtual_network_id = module.synapse_network.vnet_id

  provider = azurerm.tooling
}

resource "azurerm_virtual_network_peering" "odw_to_tooling_failover" {
  name                      = "pins-peer-${local.service_name}-${module.azure_region.paired_location.location_short}-to-tooling-${var.environment}"
  resource_group_name       = azurerm_resource_group.network_failover.name
  virtual_network_name      = module.synapse_network_failover.vnet_name
  remote_virtual_network_id = data.azurerm_virtual_network.tooling.id
}

resource "azurerm_virtual_network_peering" "tooling_to_odw_failover" {
  name                      = "pins-peer-tooling-to-${local.service_name}-${module.azure_region.paired_location.location_short}-${var.environment}"
  resource_group_name       = var.tooling_config.network_rg
  virtual_network_name      = var.tooling_config.network_name
  remote_virtual_network_id = module.synapse_network_failover.vnet_id

  provider = azurerm.tooling
}

# network links to tooling

data "azurerm_private_dns_zone" "tooling_key_vault" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = var.tooling_config.network_rg

  provider = azurerm.tooling
}

data "azurerm_private_dns_zone" "tooling_synapse" {
  name                = "privatelink.azuresynapse.net"
  resource_group_name = var.tooling_config.network_rg

  provider = azurerm.tooling
}

data "azurerm_private_dns_zone" "tooling_synapse_dev" {
  name                = "privatelink.dev.azuresynapse.net"
  resource_group_name = var.tooling_config.network_rg

  provider = azurerm.tooling
}

locals {
  storage_zones = ["blob", "dfs", "file", "queue", "table", "web"]
}

data "azurerm_private_dns_zone" "tooling_storage" {
  for_each = toset(local.storage_zones)

  name                = "privatelink.${each.key}.core.windows.net"
  resource_group_name = var.tooling_config.network_rg

  provider = azurerm.tooling
}

