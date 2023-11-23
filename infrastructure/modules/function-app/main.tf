resource "azurerm_linux_function_app" "function" {
  name                        = "pins-${var.function_app_name}-${local.resource_suffix}"
  resource_group_name         = var.resource_group_name
  location                    = var.location
  service_plan_id             = var.app_service_plan_id
  storage_account_name        = var.storage_account_name
  storage_account_access_key  = var.storage_account_access_key
  https_only                  = true
  tags                        = local.tags
  functions_extension_version = var.functions_extension_version
  auth_settings {
    enabled = var.auth_settings["enabled"]
  }

  app_settings = var.app_settings

  site_config {
    always_on = local.site_config["always_on"]
    cors {
      allowed_origins     = local.site_config.cors["allowed_origins"]
      support_credentials = local.site_config.cors["support_credentials"]
    }

    application_stack {
      python_version          = local.site_config.application_stack["python_version"]
      powershell_core_version = local.site_config.application_stack["powershell_core_version"] 
      java_version            = local.site_config.application_stack["java_version"] 
      dotnet_version          = local.site_config.application_stack["dotnet_version"]
    }
    ftps_state                  = local.site_config["ftps_state"] == "AllAllowed" ? "FtpsOnly" : local.site_config["ftps_state"]
    health_check_path           = local.site_config["health_check_path"]
    http2_enabled               = local.site_config["http2_enabled"]
    linux_fx_version            = local.site_config["linux_fx_version"]
    minimum_tls_version         = local.site_config["minimum_tls_version"]
    pre_warmed_instance_count   = local.site_config["pre_warmed_instance_count"]
    scm_use_main_ip_restriction = local.site_config["scm_use_main_ip_restriction"]
    use_32_bit_worker           = local.site_config["use_32_bit_worker"]
    websockets_enabled          = local.site_config["websockets_enabled"]
    vnet_route_all_enabled      = local.site_config["vnet_route_all_enabled"]
    dynamic "ip_restriction" {
      for_each = local.site_config.ip_restrictions.ip_addresses
      iterator = ip_addresses
      content {
        ip_address = ip_addresses.value["ip_address"]
        name       = ip_addresses.value["rule_name"]
        priority   = ip_addresses.value["priority"]
        action     = ip_addresses.value["action"]
      }
    }
    dynamic "ip_restriction" {
      for_each = local.site_config.ip_restrictions.service_tags
      iterator = service_tags
      content {
        service_tag = service_tags.value["service_tag_name"]
        name        = service_tags.value["rule_name"]
        priority    = service_tags.value["priority"]
        action      = service_tags.value["action"]
      }
    }
    dynamic "ip_restriction" {
      for_each = local.site_config.ip_restrictions.subnet_ids
      iterator = subnet_ids
      content {
        virtual_network_subnet_id = subnet_ids.value["subnet_id"]
        name                      = subnet_ids.value["rule_name"]
        priority                  = subnet_ids.value["priority"]
        action                    = subnet_ids.value["action"]
      }
    }
  }
  identity {
    type         = length(var.identity_ids) == 0 ? "SystemAssigned" : "UserAssigned"
    identity_ids = length(var.identity_ids) == 0 ? null : var.identity_ids
  }
}
