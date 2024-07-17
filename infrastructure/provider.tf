terraform {
  backend "azurerm" {
    # Per-environment key specified in ./environments/*.tfbackend
    container_name       = "terraformstate-odw"
    resource_group_name  = "pins-rg-shared-terraform-uks"
    subscription_id      = "edb1ff78-90da-4901-a497-7e79f966f8e2"
    storage_account_name = "pinsstsharedtfstateuks"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.74.0"
    }
  }
  required_version = ">= 1.1.6, < 3.74.0"
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.odt_subscription_id
  alias           = "odt"
}

provider "azurerm" {
  features {}
  subscription_id = var.horizon_subscription_id
  alias           = "horizon"
}
