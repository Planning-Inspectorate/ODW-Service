resource "azurerm_servicebus_namespace" "synapse" {
  name                = "sb-${local.resource_suffix}-${random_string.unique_id.id}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = var.service_bus_failover_enabled ? "Premium" : "Standard"
  capacity            = var.service_bus_failover_enabled ? 1 : 0

  tags = local.tags
}
