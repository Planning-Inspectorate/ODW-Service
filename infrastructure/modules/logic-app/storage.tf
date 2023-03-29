resource "azurerm_storage_account" "logic_app" {
  #checkov:skip=CKV_AZURE_35: Firewall not required for this storage account
  #checkov:skip=CKV_AZURE_59: Firewall not required for this storage account
  #checkov:skip=CKV_AZURE_190: Firewall not required for this storage account
  #checkov:skip=CKV_AZURE_206: Locally redundant storage is acceptable for this storage account use-case
  #checkov:skip=CKV2_AZURE_1: Microsoft managed keys are acceptable
  #checkov:skip=CKV2_AZURE_8: Firewall not required for this storage account
  #checkov:skip=CKV2_AZURE_18: Microsoft managed keys are acceptable
  name                     = replace("pins-st-${local.resource_suffix}-${random_string.unique_id.id}", "-", "")
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  tags                     = local.tags
}
