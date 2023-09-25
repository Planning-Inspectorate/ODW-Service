locals {
  module_name     = "api-management"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  apim_apis_defaults = {
    revision              = "1"
    protocols             = ["https"]
    subscription_required = true
  }

  apim_apis = { for v in var.apim_apis : v.name => merge(local.apim_apis_defaults, v) }

  apim_products_defaults = {
    subscription_required = true
    approval_required     = false
    published             = true
  }

  apim_products = { for v in var.apim_products : v.product_id => merge(local.apim_products_defaults, v) }

  apim_api_policies_defaults = {
    content_format = "rawxml-link"
  }

  apim_api_policies = { for v in var.apim_api_policies : v.api_name => merge(local.apim_api_policies_defaults, v) }

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )
}
