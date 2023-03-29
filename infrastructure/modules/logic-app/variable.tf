variable "app_service_plan_enabled" {
  default     = false
  description = "Determines whether an App Service Plan should be deployed"
  type        = bool
}

variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "location" {
  description = "The short-format Azure region into which resources will be deployed"
  type        = string
}

variable "logic_app_standard_enabled" {
  default     = false
  description = "Determines whether a Logic App Standard function should be deployed"
  type        = bool
}

variable "logic_app_storage_account" {
  description = "The name of the storage account used by the Logic App"
  type        = string
}

variable "logic_app_storage_account_access_key" {
  description = "The access key for the storage account"
  type        = string
  sensitive   = true
}

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
