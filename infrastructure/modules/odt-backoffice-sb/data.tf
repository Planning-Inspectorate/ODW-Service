data "azurerm_resources" "odt_pe_backoffice_sb" {
  resource_group_name = var.odt_back_office_service_bus_resource_group_name
  name                = var.odt_back_office_service_bus_name
  type                = "Microsoft.ServiceBus/namespaces"

  provider = azurerm.odt
}

data "azurerm_servicebus_topic" "topic_id" {
  count        = length(local.odt_backoffice_sb_topic_names)
  name         = local.odt_backoffice_sb_topic_names[count.index]
  namespace_id = data.azurerm_resources.odt_pe_backoffice_sb.resources[0].id

  provider = azurerm.odt
}

data "azurerm_servicebus_topic" "topics_to_send" {
  for_each = toset(var.topics_to_send)

  name         = each.value
  namespace_id = data.azurerm_resources.odt_pe_backoffice_sb.resources[0].id

  provider = azurerm.odt
}

data "azuread_group" "groups" {
  count        = length(local.group_names)
  display_name = local.group_names[count.index]
}

data "azuread_user" "users" {
  count               = length(local.user_principal_names)
  user_principal_name = local.user_principal_names[count.index]
}

data "azuread_service_principal" "service_principals" {
  count        = length(local.service_principal_names)
  display_name = local.service_principal_names[count.index]
}
