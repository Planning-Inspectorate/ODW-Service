locals {
  location     = var.location
  service_name = "odw"

  data_lake_config_files_path = "${path.module}/configuration/data-lake"
  firewall_config_file_path   = "${path.module}/configuration/firewall-rules/allowed_ip_addresses.yaml"
  lifecycle_policy_file_path  = "${path.module}/configuration/data-lifecycle/policies.json"

  resource_suffix          = "${local.service_name}-${var.environment}-${module.azure_region.location_short}"
  resource_suffix_failover = "${local.service_name}-${var.environment}-${module.azure_region.paired_location.location_short}"
  resource_suffix_global   = "${local.service_name}-${var.environment}-global"

  apim_subnet_name    = "ApimSubnet"
  compute_subnet_name = "ComputeSubnet"
  synapse_subnet_name = "SynapseEndpointSubnet"

  tags = merge(
    var.tags,
    {
      CreatedBy   = "Terraform"
      Environment = var.environment
      ServiceName = local.service_name
    }
  )
}
