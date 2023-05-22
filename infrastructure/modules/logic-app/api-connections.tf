resource "azurerm_resource_group_template_deployment" "service_bus_3" {
  name                = "servicebus-3"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/servicebus-3.json")
  parameters_content = jsonencode({
    "service_bus_connection_name" = {
      value = "servicebus-3"
    }
    "service_bus_api_id" = {
      value = module.synapse_ingestion.service_bus_namespace_id
    }
    "location" = {
      value = var.location
    }
  })
  deployment_mode = "Incremental"
}

resource "azurerm_resource_group_template_deployment" "zendesk" {
  name                = "zendesk"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/zendesk.json")
  deployment_mode  = "Incremental"
}
