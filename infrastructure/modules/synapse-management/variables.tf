variable "data_lake_account_id" {
  description = "The ID of the Data Lake Storage Account"
  type        = string
}

variable "link_purview" {
  default     = true
  description = "Determines whether Purview will be linked to"
  type        = bool
}

variable "devops_agent_subnet_name" {
  default     = "ComputeSubnet"
  description = "The name of the subnet into which the devops agents will be deployed"
  type        = string
}

variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "firewall_allowed_ip_addresses" {
  default     = []
  description = "A list of CIDR ranges to be permitted access to the data lake Storage Account"
  type        = list(string)
}

variable "key_vault_private_endpoint_dns_zone_id" {
  description = "The ID of the Private DNS Zone hosting privatelink.vaultcore.azure.net"
  type        = string
}

variable "key_vault_role_assignments" {
  default     = {}
  description = "An object mapping RBAC roles to principal IDs for Key Vault"
  type        = map(list(string))
}

variable "network_resource_group_name" {
  description = "The name of the resource group into which private endpoints will be deployed"
  type        = string
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

variable "synapse_private_endpoint_subnet_name" {
  default     = "SynapseEndpointSubnet"
  description = "The name of the subnet into which Synapse private endpoints should be deployed"
  type        = string
}

variable "tags" {
  default     = {}
  description = "A collection of tags to assign to taggable resources"
  type        = map(string)
}

variable "vnet_subnet_ids" {
  description = "A map of subnet names and IDs comprising the linked Virtual Network"
  type        = map(string)
}

variable "vnet_subnet_ids_failover" {
  description = "A map of subnet names and IDs comprising the linked Virtual Network"
  type        = map(string)
}

variable "purview_msi_id" {
  description = "The id of the Purview MSI"
  type        = string
}
