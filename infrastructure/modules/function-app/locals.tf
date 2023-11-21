/*
    Terraform configuration file defining provider configuration
*/
locals {
  module_name     = "function-app"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )

  application_stack = merge(
    var.application_stack_defaults,
    var.application_stack
  )
  site_config = merge(
    var.site_config_defaults,
    var.site_config
  )
}
