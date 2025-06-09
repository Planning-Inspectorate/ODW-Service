resource "azurerm_resource_group" "shir" {
  name     = "pins-rg-shir-${local.resource_suffix}"
  location = module.azure_region.location_cli

  tags = local.tags
}

resource "azurerm_resource_group" "shir_failover" {
  count = var.failover_deployment ? 1 : 0

  name     = "pins-rg-shir-${local.resource_suffix_failover}"
  location = module.azure_region.paired_location.location_cli

  tags = local.tags
}

module "synapse_shir" {
  source = "./modules/synapse-shir"

  environment         = var.environment
  resource_group_name = azurerm_resource_group.shir.name
  location            = module.azure_region.location_cli
  service_name        = local.service_name

  devops_agent_subnet_name = local.compute_subnet_name
  synapse_workspace_id     = module.synapse_workspace_private.synapse_workspace_id
  vnet_subnet_ids          = module.synapse_network.vnet_subnets

  tags = local.tags

  run_shir_setup_script = var.run_shir_setup_script
}

module "synapse_shir_failover" {
  count = var.failover_deployment ? 1 : 0

  source = "./modules/synapse-shir"

  environment         = var.environment
  resource_group_name = azurerm_resource_group.shir_failover[0].name
  location            = module.azure_region.paired_location.location_cli
  service_name        = local.service_name

  devops_agent_subnet_name = local.compute_subnet_name
  synapse_workspace_id     = module.synapse_workspace_private_failover[0].synapse_workspace_id
  vnet_subnet_ids          = module.synapse_network_failover.vnet_subnets

  tags = local.tags

  run_shir_setup_script = var.run_shir_setup_script
}
