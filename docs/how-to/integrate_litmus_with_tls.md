# Integrate Litmus with TLS

This how-to guide outlines the process of integrating Charmed Litmus with TLS in order to ensure encrypted communication across both internal service interactions and external client connections.
TLS integration can be done as both Day 1 and Day 2 operation.

In this how-to we will use [self-signed-certificates charm] to provide necessary TLS certificates.

```{note}
Using self-signed TLS certificates is discouraged for the production environments.
```

## 1. Add self-signed-certificates to your Charmed Chaos Engineering platform Terraform module

Update your solution Terraform module (here it's named `main.tf`):

```console
cat << EOF > main.tf
module "self-signed-certificates" {
  source   = "git::https://github.com/canonical/self-signed-certificates-operator//terraform"
  model    = data.juju_model.charmed-chaos.name
  channel  = var.self_signed_certificates_channel
  base     = "ubuntu@24.04"
  config   = var.self_signed_certificates_config
}

resource "juju_integration" "litmus-auth-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.auth_app_name
    endpoint = module.charmed-litmus.auth_tls_certificates_endpoint
  }

  application {
    offer_url = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-backend-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.backend_app_name
    endpoint = module.charmed-litmus.backend_tls_certificates_endpoint
  }

  application {
    offer_url = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-chaoscenter-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.chaoscenter_app_name
    endpoint = module.charmed-litmus.chaoscenter_tls_certificates_endpoint
  }

  application {
    offer_url = module.self-signed-certificates.provides.certificates
  }
}

EOF
```

```{note}
In this guide it is assumed, that the Terraform module responsible for deploying Charmed Chaos Engineering platform is named `charmed-chaos`.
If you use different name, please make sure to update the code above.
```

## 2. Apply the changes

Fetch `self-signed-certificates` module:

```console
terraform init
```

Apply new configuration:

```console
terraform apply -auto-approve
```

Successful integration is indicated by the change of `ChaosCenter` URL printed in `juju status` output. Example:

```console
Unit                   Workload  Agent  Address       Ports  Message
(...)        
litmus-chaoscenter/0*  active    idle   10.1.194.255         Ready at https://litmus-chaoscenter.charmed-chaos.svc.cluster.local:8185.
(...)
```

## 3. Example of a complete solution Terraform module including Charmed Litmus integrated with TLS

```console
resource "juju_model" "charmed-chaos" {
  name = "charmed-chaos"
}

module "charmed-litmus" {
  source = "git::https://github.com/canonical/litmus-operators//terraform"

  model      = juju_model.charmed-chaos.name
  depends_on = [juju_model.charmed-chaos]
}

module "self-signed-certificates" {
  source   = "git::https://github.com/canonical/self-signed-certificates-operator//terraform"
  model    = data.juju_model.charmed-chaos.name
  channel  = var.self_signed_certificates_channel
  base     = "ubuntu@24.04"
  config   = var.self_signed_certificates_config
}

resource "juju_integration" "litmus-auth-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.auth_app_name
    endpoint = module.charmed-litmus.auth_tls_certificates_endpoint
  }

  application {
    offer_url = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-backend-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.backend_app_name
    endpoint = module.charmed-litmus.backend_tls_certificates_endpoint
  }

  application {
    offer_url = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-chaoscenter-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.chaoscenter_app_name
    endpoint = module.charmed-litmus.chaoscenter_tls_certificates_endpoint
  }

  application {
    offer_url = module.self-signed-certificates.provides.certificates
  }
}
```

[self-signed-certificates charm]: https://charmhub.io/self-signed-certificates
