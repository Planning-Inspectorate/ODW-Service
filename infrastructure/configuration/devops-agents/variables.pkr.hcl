variable "client_id" {
  description = "The ID of the service principal used to build the image"
  type        = string
}

variable "client_secret" {
  description = "The client secret of the service principal used to build the image"
  type        = string
}

variable "image_prefix" {
  default     = "devops-agents"
  description = "The name for the image which will be created"
  type        = string
}

variable "location" {
  default     = "UK South"
  description = "The Azure region in which to provision temporary resources"
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group where the image will be created"
  type        = string
}

variable "subscription_id" {
  description = "The ID of the subscription containing the service principal used to build the image"
  type        = string
}

variable "tenant_id" {
  description = "The ID of the tenant containing the service principal used to build the image"
  type        = string
}
