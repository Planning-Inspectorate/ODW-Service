packer {
  required_plugins {
    azure = {
      source  = "github.com/hashicorp/azure"
      version = "~> 2"
    }
  }
}

build {
  name = "azure-devops-agents"

  source "source.azure-arm.azure-agents" {
    managed_image_resource_group_name = var.resource_group_name
    managed_image_name                = "${var.image_prefix}-${formatdate("YYYYMMDDhhmmss",timestamp())}"

    os_type         = "Linux"
    image_publisher = "canonical"
    image_offer     = "0001-com-ubuntu-server-focal"
    image_sku       = "20_04-lts"

    location        = var.location
    vm_size         = "Standard_D2ds_v5"
  }

  provisioner "shell" {
    execute_command = "chmod +x {{ .Path }}; {{ .Vars }} sudo -E bash -e '{{ .Path }}'"
    script          = "${path.cwd}/tools.sh"
  }
}

source "azure-arm" "azure-agents" {
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
}

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

