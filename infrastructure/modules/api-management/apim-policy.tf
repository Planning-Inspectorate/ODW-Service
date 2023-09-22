resource "azurerm_api_management_api_policy" "api_management_api_policy" {
  for_each = local.apim_api_policies

  api_name            = each.key
  api_management_name = azurerm_api_management.api_management.name
  resource_group_name = var.resource_group_name
  xml_content         = file("${path.module}/policies/${each.value.xml_content}")
}
