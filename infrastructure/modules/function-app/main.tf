resource "azurerm_linux_function_app" "function" {
  name                          = "pins-${var.function_app_name}-${local.resource_suffix}"
  resource_group_name           = var.resource_group_name
  location                      = var.location
  service_plan_id               = var.service_plan_id
  storage_account_name          = var.storage_account_name
  storage_account_access_key    = var.storage_account_access_key
  https_only                    = true
  tags                          = local.tags
  public_network_access_enabled = false
  functions_extension_version   = var.functions_extension_version
  virtual_network_subnet_id     = var.synapse_vnet_subnet_names[var.synapse_function_app_subnet_name]
  app_settings                  = var.app_settings
  auth_settings {
    enabled = var.auth_settings["enabled"]
  }
  site_config {}
  identity {
    type         = length(var.identity_ids) == 0 ? "SystemAssigned" : "UserAssigned"
    identity_ids = length(var.identity_ids) == 0 ? null : var.identity_ids
  }
}
