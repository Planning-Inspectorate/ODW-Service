locals {
  location     = var.location
  service_name = "odw"

  resource_suffix     = "${local.service_name}-${var.environment}-${module.azure_region.location_short}"
  synapse_subnet_name = "SynapseEndpointSubnet"

  tags = merge(
    var.tags,
    {
      CreatedBy    = "Terraform"
      DeployedDate = timestamp()
      Environment  = var.environment
      ServiceName  = local.service_name
    }
  )
}
