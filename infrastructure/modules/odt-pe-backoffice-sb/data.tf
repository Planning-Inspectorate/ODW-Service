data "azurerm_resources" "odt_pe_backoffice_rg" {
  provider            = azurerm.odt_backoffice
  resource_group_name = local.resource_group
  type                = "Microsoft.ServiceBus/namespaces"
}

data "azurerm_servicebus_namespace" "odt_pe_backoffice_sb" {
  provider            = azurerm.odt_backoffice
  name                = data.azurerm_resources.odt_pe_backoffice_rg.resources.name
  resource_group_name = local.resource_group
}