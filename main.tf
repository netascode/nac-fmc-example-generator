terraform {
  required_providers {
    fmc = {
      source  = "CiscoDevNet/fmc"
    }
  }
}

provider "fmc" {
  url      = ""
  username = ""
  password = ""
}

module "nac-fmc" {
  source  = "netascode/nac-fmc/fmc"
  version = "0.1.2"
  yaml_directories = ["data"]
}
