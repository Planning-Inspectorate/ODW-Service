variable "api_connection_servicebus_enabled" {
  default     = false
  description = "Determines whether a Logic App Standard function should be deployed"
  type        = bool
}

variable "api_connection_zendesk_enabled" {
  default     = false
  description = "Determines whether a Logic App Standard function should be deployed"
  type        = bool
}

variable "connection_string_servicebus" {
  default     = "https://363f4178262a1d08.12.common.logic-uksouth.azure-apihub.net/apim/servicebus/32eeb0120347401eb61c2e2ba18188f8"
  description = "The connection string for the servicebus api resource"
  type        = string
}

variable "connection_string_zendesk" {
  default     = "https://363f4178262a1d08.12.common.logic-uksouth.azure-apihub.net/apim/zendesk/27b0df658eb24f1fbc0e9287b57c6074"
  description = "The connection string for the zendesk api resource"
  type        = string
}

variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "location" {
  description = "The short-format Azure region into which resources will be deployed"
  type        = string
}

variable "logic_app_service_plan_enabled" {
  default     = false
  description = "Determines whether an App Service Plan should be deployed"
  type        = bool
}

variable "logic_app_standard_enabled" {
  default     = false
  description = "Determines whether a Logic App Standard function should be deployed"
  type        = bool
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

variable "workflow_zendesk_created_enabled" {
  default     = false
  description = "Determines whether Workflow zendesk-created will be deployed"
  type        = bool
}

variable "workflow_zendesk_updated_enabled" {
  default     = false
  description = "Determines whether Workflow zendesk-updated will be deployed"
  type        = bool
}
