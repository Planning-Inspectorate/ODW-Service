variable "alert_group_platform_enabled" {
  default     = false
  description = "Determines whether the alert group for platform alerts is enabled"
  type        = bool
}

variable "alert_group_synapse_enabled" {
  default     = false
  description = "Determines whether the alert group for Synapse alerts is enabled"
  type        = bool
}

variable "alert_scope_service_health" {
  description = "The resource scope at which to alert on service health events"
  type        = string
}

variable "alert_threshold_data_lake_capacity_bytes" {
  default     = 1099511627776 # 1TiB
  description = "The threshold at which to trigger an alert for exceeding Data Lake capacity in bytes"
  type        = number
}

variable "data_lake_account_id" {
  description = "The ID of the Data Lake Storage Account from which to collect diagnostic logs"
  type        = string
}

variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "function_app_ids" {
  description = "A map of Function App names to their respective IDs"
  type        = map(string)
}

variable "key_vault_id" {
  description = "The ID of the Key Vault from which to collect diagnostic logs"
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

variable "log_retention_days" {
  default     = 30
  description = "The number of days to retain logs in the Log Analytics Workspace"
  type        = number
}

variable "service_bus_namespace_id" {
  description = "The ID of the Service Bus Namespace from which to collect diagnostic logs"
  type        = string
}

variable "service_name" {
  description = "The short-format name of the overarching service being deployed"
  type        = string
}

variable "spark_pool_enabled" {
  default     = false
  description = "Determines whether a Synapse-linked Spark pool is deployed and should be monitored"
  type        = bool
}

variable "sql_pool_enabled" {
  default     = false
  description = "Determines whether a Synapse-linked dedicated SQL pool is deployed and should be monitored"
  type        = bool
}

variable "synapse_spark_pool_id" {
  default     = null
  description = "The ID of the Synapse Spark Pool from which to collect diagnostic logs"
  type        = string
}

variable "synapse_sql_pool_id" {
  default     = null
  description = "The ID of the Synapse Dedicated SQL Pool from which to collect diagnostic logs"
  type        = string
}

variable "synapse_workspace_id" {
  description = "The ID of the Synapse Workspace from which to collect diagnostic logs"
  type        = string
}

variable "synapse_vnet_id" {
  description = "The ID of the Synapse Virtual network from which to collect diagnostic logs"
  type        = string
}

variable "tags" {
  default     = {}
  description = "A collection of tags to assign to taggable resources"
  type        = map(string)
}
