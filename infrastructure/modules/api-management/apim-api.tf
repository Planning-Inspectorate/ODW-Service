resource "azurerm_api_management_api" "api" {
  for_each = local.apim_apis

  name                  = each.key
  resource_group_name   = var.resource_group_name
  api_management_name   = azurerm_api_management.api_management.name
  revision              = each.value.revision
  display_name          = each.value.display_name
  path                  = each.value.path
  protocols             = each.value.protocols
  service_url           = each.value.service_url
  subscription_required = each.value.subscription_required

  import {
    content_format = each.value.content_format
    content_value  = file("${path.module}/api/${each.value.content_value}")
  }
}

resource "azurerm_api_management_product_api" "api_management_product_api" {
  for_each = {
    for product_id in local.apim_products : product_id.name => product_id
  }

  product_id          = each.value.product_id
  api_name            = azurerm_api_management_api.api[each.key].name
  api_management_name = azurerm_api_management.api_management.name
  resource_group_name = var.resource_group_name
}
