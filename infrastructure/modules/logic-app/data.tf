data "azurerm_managed_api" "zendesk_managed_api" {
  location = var.location
  name     = "zendesk"
}

data "azurerm_managed_api" "service_bus_managed_api" {
  location = var.location
  name     = "servicebus"
}

data "azapi_resource" "zendesk_custom_api" {
  parent_id = var.resource_group_id
  name      = "zendesk-custom-api"
  type      = "Microsoft.Web/customApis@2016-06-01"
}
