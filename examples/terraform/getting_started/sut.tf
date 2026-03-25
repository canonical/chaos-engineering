# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

resource "juju_model" "self-signed-certs-test" {
  name = "self-signed-certs-test"
}

module "self-signed-certificates" {
  source = "git::https://github.com/canonical/self-signed-certificates-operator//terraform"

  model_uuid = juju_model.self-signed-certs-test.uuid
  depends_on = [juju_model.self-signed-certs-test]
}

module "litmus-infrastructure" {
  source = "git::https://github.com/canonical/litmus-operators//infrastructure/terraform"

  channel = "dev/edge"

  model_uuid = juju_model.self-signed-certs-test.uuid
  depends_on = [juju_model.self-signed-certs-test]
}

resource "juju_offer" "litmus-infrastructure-offer" {
  model_uuid       = juju_model.self-signed-certs-test.uuid
  application_name = module.litmus-infrastructure.app_name
  endpoints = [module.litmus-infrastructure.endpoints.litmus-infrastructure]
}
