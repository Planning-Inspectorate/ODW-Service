#!/bin/bash
APT_REPOSITORIES=(
  "main"
  "restricted"
  "universe"
  "multiverse"
)

COMMON_PACKAGES=(
  "build-essential"
  "jq"
  "unzip"
  "xvfb"
  "python3-pip"
)

TFENV_VERSION="3.0.0"

TERRAFORM_VERSIONS=("1.7.3" "1.9.0")
DEFAULT_TERRAFORM_VERSION="1.9.0"

CHECKOV_VERSION="2.2.94"
