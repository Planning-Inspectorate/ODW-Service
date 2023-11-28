locals {
  module_name     = "storage-account"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )

  cicd_subnet_ids = module.synapse_network.vnet_subnet_ids

  soft_delete_retention_policy = var.soft_delete_retention_policy == true || substr(var.environment, 0, 2) == "production" ? true : var.soft_delete_retention_policy

}
