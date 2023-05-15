variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "location" {
  description = "The short-format Azure region into which resources will be deployed"
  type        = string
}

variable "logic_app_enabled" {
  default     = false
  description = "Determines whether the resources for the App Service Plan, Storage Account and Logic App Standard should be deployed"
  type        = bool
}

# variable "logic_app_id" {
#   description = "The name of the Logic App"
#   type        = string
# }

# variable "logic_app_id_failover" {
#   description = "The name of the Logic App for backup and failover"
#   type        = string
# }

variable "resource_group_name" {
  description = "The name of the resource group into which resources will be deployed"
  type        = string
}

variable "service_name" {
  description = "The short-format name of the overarching service being deployed"
  type        = string
}

variable "sku_name" {
  default     = "WS1"
  description = "The SKU of the App Service Plan"
  type        = string
}

variable "tags" {
  default     = {}
  description = "A collection of tags to assign to taggable resources"
  type        = map(string)
}
