data "azurerm_purview_account" "management" {
  count = var.deploy_purview ? 1 : 0

  name                        = "pins-pview-"
  resource_group_name         = "pins-rg-datamgmt"
}

resource "azurerm_role_assignment" "purview_storage" {
  count = var.deploy_purview ? 1 : 0

  scope                = var.data_lake_account_id
  role_definition_name = "Storage Blob Data Owner"
  principal_id         = data.azurerm_purview_account.management[0].identity[0].principal_id
}
