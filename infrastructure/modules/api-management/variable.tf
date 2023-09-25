variable "apim_apis" {
  description = "A map of API names to API Management API objects"
  type        = list(map(string))
}

variable "apim_api_policies" {
  description = "A map of API names to API Management API policy XML files"
  type        = map(string)
}

variable "apim_products" {
  description = "A map of product IDs to API Management product objects"
  type        = map(string)
}

variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "location" {
  description = "The short-format Azure region into which resources will be deployed"
  type        = string
}

# variable "key_vault_id" {
#   description = "The ID of the Key Vault to use for secret storage"
#   type        = string
# }

variable "publisher_email" {
  description = "The email address of the publisher of the API Management instance"
  type        = string
}

variable "publisher_name" {
  description = "The name of the publisher of the API Management instance"
  type        = string
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
  description = "The SKU name of the API Management instance"
  type        = string
}

variable "synapse_apim_subnet_name" {
  default     = "ApimSubnet"
  description = "The name of the subnet into which the Bastion jumpbox VM should be deployed"
  type        = string
}

# variable "synapse_vnet_security_groups" {
#   description = "A map of subnet names to network security group IDs"
#   type        = map(string)
# }

variable "synapse_vnet_subnet_names" {
  description = "A map of subnet names to IDs comprising the linked Virtual Network for Bastion host deployment"
  type        = map(string)
}

# variable "synapse_vnet_subnet_prefixes" {
#   description = "A map of subnet names to CIDR ranges"
#   type        = map(string)
# }

variable "tags" {
  default     = {}
  description = "A collection of tags to assign to taggable resources"
  type        = map(string)
}
