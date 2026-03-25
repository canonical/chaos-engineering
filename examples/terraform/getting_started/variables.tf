# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

variable "admin_password" {
  description = "The password to set for the Litmus admin user."
  type        = string
  sensitive   = true
}

variable "charm_password" {
  description = "The password to set for the Litmus charm bot user."
  type        = string
  sensitive   = true
}
