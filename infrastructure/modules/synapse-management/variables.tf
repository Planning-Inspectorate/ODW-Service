variable "deploy_purview" {
  default     = true
  description = "Determines whether Purview will be deployed"
  type        = bool
}

variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "key_vault_role_assignments" {
  default     = {}
  description = "An object mapping RBAC roles to principal IDs for Key Vault"
  type        = map(list(string))
}

variable "resource_group_name" {
  description = "The name of the resource group into which resources will be deployed"
  type        = string
}

variable "location" {
  description = "The short-format Azure region into which resources will be deployed"
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
