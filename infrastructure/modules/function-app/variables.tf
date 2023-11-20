/*
    Terraform configuration file defining variables
*/
variable "environment" {
  type        = string
  description = "The environment name. Used as a tag and in naming the resource group"
}

variable "location" {
  type        = string
  description = "The region resources will be deployed to"
  default     = "northeurope"
}

variable "tags" {
  description = "List of tags to be applied to resources"
  type        = map(string)
  default     = {}
}

variable "resource_group_name" {
  type        = string
  description = "The target resource group this module should be deployed into. If not specified one will be created for you with name like: environment-application-template-location"
  default     = ""
}

variable "function_app_name" {
  type        = string
  description = "Name of the function app"
}

# app service plan related

variable "app_service_plan_id" {
  type        = string
  description = "ID of the app service plan instance to host this app service. If unspecified one will be created for you"
  default     = null
}

variable "identity_ids" {
  type        = list(string)
  description = "List of service principal IDs if you want to use a User Assigned Identity over a System Assigned Identity"
  default     = []
}

variable "service_name" {
  type        = string
  description = "Name of the service"
}

variable "storage_account_name" {
  type        = string
  description = "The name of the backend storage account"
  default     = null
}

variable "storage_account_access_key" {
  type        = string
  description = "The key to access the backend storage account"
  default     = null
  sensitive   = true
}

variable "function_version" {
  type        = string
  description = "The function version. ~1 through ~4"
  default     = "~3"
}

variable "auth_settings" {
  type        = map(string)
  description = "Function app auth settings"
  default = {
    enabled = true
  }
}

variable "app_settings" {
  type        = map(string)
  description = "Function app settings"
  default     = {}
}

variable "site_config_defaults" {
  type = object({
    always_on = bool
    cors = object({
      allowed_origins     = list(string)
      support_credentials = bool
    })
    ftps_state                  = string
    health_check_path           = string
    http2_enabled               = bool
    java_version                = string
    linux_fx_version            = string
    dotnet_framework_version    = string
    min_tls_version             = string
    pre_warmed_instance_count   = number
    scm_ip_restriction          = list(any)
    scm_type                    = string
    scm_use_main_ip_restriction = bool
    use_32_bit_worker_process   = bool
    websockets_enabled          = bool
    vnet_route_all_enabled      = bool
    ip_restrictions = object({
      ip_addresses = list(object({
        rule_name  = string
        ip_address = string
        priority   = number
        action     = string
      }))
      service_tags = list(object({
        rule_name        = string
        service_tag_name = string
        priority         = number
        action           = string
      }))
      subnet_ids = list(object({
        rule_name = string
        subnet_id = string
        priority  = number
        action    = string
      }))
    })
  })
  description = "A site config block for configuring the function"
  default = {
    always_on = true
    cors = {
      allowed_origins     = ["*"]
      support_credentials = false
    }
    ftps_state                  = "Disabled"
    health_check_path           = null
    http2_enabled               = true
    java_version                = null
    linux_fx_version            = null
    dotnet_framework_version    = "v4.0"
    min_tls_version             = 1.2
    pre_warmed_instance_count   = null
    scm_ip_restriction          = []
    scm_type                    = "None"
    scm_use_main_ip_restriction = true
    use_32_bit_worker_process   = false
    websockets_enabled          = true
    vnet_route_all_enabled      = false
    ip_restrictions = {
      ip_addresses = []
      service_tags = []
      subnet_ids   = []
    }
  }
}

variable "site_config" {
  type        = any
  description = "Site config to override site_config_defaults. Object structure identical to site_config_defaults"
  default     = {}
}
