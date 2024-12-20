terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0, < 5.0"
    }
    azapi = {
      source  = "azure/azapi"
      version = "~> 1.7.0"
    }
  }
  required_version = ">= 1.5.7, < 1.10.0"
}
