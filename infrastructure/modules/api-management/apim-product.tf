resource "azurerm_api_management_product" "api_management_product" {
  for_each = local.apim_products

  product_id            = each.key
  api_management_name   = azurerm_api_management.api_management.name
  resource_group_name   = var.resource_group_name
  display_name          = each.value.display_name
  description           = each.value.description
  subscription_required = each.value.subscription_required
  approval_required     = each.value.approval_required
  published             = each.value.published
}
