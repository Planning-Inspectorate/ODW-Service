resource "azurerm_resource_group_template_deployment" "service_bus" {
  name                = "servicebus-1"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/servicebus.json")
  parameters_content = jsonencode({
    "service_bus_connection_name" = {
      value = "servicebus-1"
    }
    "service_bus_connection_string" = {
      value = "https://pins-sb-odw-dev-uks-b9rt9m.servicebus.windows.net:443/"
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
