# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

resource "juju_model" "charmed-chaos" {
  name = "charmed-chaos"
}

module "charmed-litmus" {
  source = "git::https://github.com/canonical/litmus-operators//terraform"

  model_uuid = juju_model.charmed-chaos.uuid
  depends_on = [juju_model.charmed-chaos]

  litmus_channel = "dev/edge"
  admin_password = var.admin_password
  charm_password = var.charm_password
}

resource "juju_integration" "litmus-infrastructure" {
  model_uuid = juju_model.charmed-chaos.uuid

  application {
    name     = module.charmed-litmus.chaoscenter_app_name
    endpoint = module.litmus-infrastructure.endpoints.litmus-infrastructure
  }

  application {
    offer_url = juju_offer.litmus-infrastructure-offer.url
  }
}
