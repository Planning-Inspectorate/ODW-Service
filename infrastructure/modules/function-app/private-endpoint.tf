resource "azurerm_private_endpoint" "function" {
  count = var.private_endpoint_enabled == true ? 1 : 0

  name                = "pins-pe-${var.function_app_name}-${local.resource_suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.synapse_vnet_subnet_names["FunctionAppSubnet"]

  private_dns_zone_group {
    name                 = "FunctionAppDnsZone"
    private_dns_zone_ids = [var.function_app_private_endpoint_dns_zone_id]
  }

  private_service_connection {
    name                           = "FunctionApp"
    is_manual_connection           = false
    private_connection_resource_id = azurerm_linux_function_app.function.id
    subresource_names              = ["sites"]
  }

  tags = local.tags
}
