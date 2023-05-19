resource "azurerm_resource_group_template_deployment" "service_bus_2" {
  name                = "servicebus-2"
  resource_group_name = var.resource_group_name

  template_content = file("${path.module}/api-connections/servicebus-2.json")
  deployment_mode  = "Incremental"
}
