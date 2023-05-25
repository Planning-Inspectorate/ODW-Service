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

variable "resource_group_name" {
  description = "The name of the resource group into which resources will be deployed"
  type        = string
}
variable "service_name" {
  description = "The short-format name of the overarching service being deployed"
  type        = string
}

variable "tags" {
  default     = {}
  description = "A collection of tags to assign to taggable resources"
  type        = map(string)
}
