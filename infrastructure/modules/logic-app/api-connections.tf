resource "azurerm_resource_group_template_deployment" "service_bus_3" {
  name                = "servicebus-3"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/servicebus-3.json")
  parameters_content = jsonencode({
    "service_bus_connection_name" = {
      value = "servicebus-3"
    }
    "service_bus_api_id" = {
      value = "/subscriptions/ff442a29-fc06-4a13-8e3e-65fd5da513b3/resourceGroups/pins-rg-ingestion-odw-dev-uks/providers/Microsoft.ServiceBus/namespaces/pins-sb-odw-dev-uks-b9rt9m"
    }
    "location" = {
      value = var.location
    }
  })
  deployment_mode = "Complete"
}

resource "azurerm_resource_group_template_deployment" "zendesk" {
  name                = "zendesk"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/zendesk.json")
  deployment_mode  = "Incremental"
}
