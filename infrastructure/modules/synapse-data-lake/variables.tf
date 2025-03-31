variable "data_lake_account_tier" {
  default     = "Standard"
  description = "The tier of the Synapse data lake Storage Account"
  type        = string
}

variable "data_lake_private_endpoint_dns_zone_id" {
  description = "The ID of the Private DNS Zone hosting privatelink.dfs.core.windows.net"
  type        = string
}

variable "data_lake_lifecycle_rules" {
  default     = []
  description = "A list of objects describing data lifecycle rules for the Synapse data lake Storage Account"
  type        = list(any)
}

variable "data_lake_replication_type" {
  default     = "ZRS"
  description = "The replication type for the Synapse data lake Storage Account"
  type        = string
}

variable "data_lake_retention_days" {
  default     = 7
  description = "The number of days blob and queue data will be retained for upon deletion"
  type        = number
}

variable "data_lake_role_assignments" {
  default     = {}
  description = "An object mapping RBAC roles to principal IDs for the data lake Storage Account"
  type        = map(list(string))
}

variable "data_lake_storage_containers" {
  default     = ["default"]
  description = "A list of container names to be created in the Synapse data lake Storage Account"
  type        = list(string)
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

variable "function_app_principal_ids" {
  description = "The principal ID's of the function app identity"
  type        = any
}

variable "function_app_subnet_name" {
  default     = "FunctionAppSubnet"
  description = "The name of the subnet into which the function apps will be deployed"
  type        = string
}

variable "horizon_integration_config" {
  description = "The configuration for integration with Horizon and associated systems"
  type = object({
    networking = object({
      resource_group_name  = string
      vnet_name            = string
      database_subnet_name = string
    })
  })
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

variable "tenant_id" {
  description = "The ID of the Azure AD tenant containing the identities used for RBAC assignments"
  type        = string
}

variable "tooling_config" {
  description = "Config for the tooling subscription dns zones"
  type = object({
    storage_private_dns_zone_id = map(string)
  })
}


variable "vnet_subnet_ids" {
  description = "A map of subnet names and IDs comprising the linked Virtual Network"
  type        = map(string)
}

variable "vnet_subnet_ids_failover" {
  description = "A map of subnet names and IDs comprising the linked Virtual Network"
  type        = map(string)
}
