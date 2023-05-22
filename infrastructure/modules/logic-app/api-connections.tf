resource "azurerm_resource_group_template_deployment" "service_bus_3" {
  name                = "servicebus-3"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/servicebus-3.json")
  deployment_mode  = "Incremental"
}

resource "azurerm_resource_group_template_deployment" "zendesk" {
  name                = "zendesk"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/zendesk.json")
  deployment_mode  = "Incremental"
}
