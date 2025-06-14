module "devops_agent_pool" {
  source = "./modules/devops-agent-pool"

  environment         = var.environment
  resource_group_name = var.devops_agent_pool_resource_group_name
  location            = module.azure_region.location_cli
  service_name        = local.service_name

  deploy_agent_pool         = var.deploy_agent_pool
  devops_agent_image_prefix = var.devops_agent_image_prefix
  devops_agent_instances    = var.devops_agent_instances
  devops_agent_subnet_name  = local.compute_subnet_name
  devops_agent_vm_sku       = var.devops_agent_vm_sku
  vnet_subnet_ids           = module.synapse_network.vnet_subnets

  tags = local.tags
}

module "devops_agent_pool_failover" {
  count  = var.devops_agent_failover_enabled ? 1 : 0
  source = "./modules/devops-agent-pool"

  environment         = var.environment
  resource_group_name = var.devops_agent_pool_resource_group_name_failover
  location            = module.azure_region.paired_location.location_cli
  service_name        = local.service_name

  deploy_agent_pool         = var.deploy_agent_pool
  devops_agent_image_prefix = var.devops_agent_image_prefix
  devops_agent_instances    = var.devops_agent_instances
  devops_agent_subnet_name  = local.compute_subnet_name
  devops_agent_vm_sku       = var.devops_agent_vm_sku
  vnet_subnet_ids           = module.synapse_network_failover.vnet_subnets

  tags = local.tags
}

moved {
  from = module.devops_agent_pool_failover.azurerm_linux_virtual_machine_scale_set.devops_agent_pool[0]
  to   = module.devops_agent_pool_failover[0].azurerm_linux_virtual_machine_scale_set.devops_agent_pool[0]
}

moved {
  from = module.devops_agent_pool_failover.azurerm_resource_group.devops_agents
  to   = module.devops_agent_pool_failover[0].azurerm_resource_group.devops_agents
}

moved {
  from = module.devops_agent_pool_failover.random_password.devops_agent_password[0]
  to   = module.devops_agent_pool_failover[0].random_password.devops_agent_password[0]
}