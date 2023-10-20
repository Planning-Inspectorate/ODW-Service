
variable "environment" {
  description = "The name of the environment in which resources will be deployed"
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group into which resources will be deployed"
  type        = string
}

variable "odt_backoffice_sb_topic_subscriptions" {
  description = "A collection of objects defining the topic subscriptions to be created"
  type = list(object({
    subscription_name                         = string
    topic_name                                = string
    status                                    = string
    max_delivery_count                        = number
    auto_delete_on_idle                       = string
    default_message_ttl                       = string
    lock_duration                             = string
    dead_lettering_on_message_expiration      = bool
    dead_lettering_on_filter_evaluation_error = bool
    enable_batched_operations                 = bool
    requires_session                          = bool
    forward_to                                = string
    role_assignments = map(object({
      users              = list(string)
      groups             = list(string)
      service_principals = list(string)
    }))
  }))
}


variable "odt_back_office_service_bus_name" {
  description = "The name of the Service Bus namespace into which resources will be deployed"
  type        = string
}

variable "odt_back_office_service_bus_resource_group_name" {
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

variable "synapse_private_endpoint_vnet_subnets" {
  description = "A map of subnet names and IDs comprising the linked Virtual Network for private endpoint deployment"
  type        = map(string)
}

variable "tags" {
  default     = {}
  description = "A collection of tags to assign to taggable resources"
  type        = map(string)
}

variable "odt_back_office_private_endpoint_dns_zone_id" {
  description = "The ID of the private DNS zone for the ODT Back Office private dns zone"
  type        = string
}
