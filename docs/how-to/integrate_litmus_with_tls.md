# Integrate Charmed Litmus with TLS

This how-to guide outlines the process of integrating Charmed Litmus with TLS in order to ensure encrypted communication across both internal service interactions and external client connections.<br>
TLS integration can be done as either Day 1 or Day 2 operation.

In this how-to we will use the [self-signed-certificates charm] to provide the necessary TLS certificates.

```{note}
For production deployments, we strongly discourage using self-signed TLS certificates. Instead, we recommend to use certificates signed by a trusted CA and safely stored, for example using a [Vault charm](https://charmhub.io/vault). 
```

## 1. Add self-signed-certificates to your Canonical Chaos Engineering platform Terraform module

```{note}
In this guide it is assumed that the Terraform module responsible for deploying the Charmed Litmus is named `charmed-litmus`.
If you use a different name, make sure to update the code below.
```

Update your solution Terraform module (in this example named `main.tf`):

```shell
cat << EOF >> main.tf
module "self-signed-certificates" {
  source   = "git::https://github.com/canonical/self-signed-certificates-operator//terraform"
  model    = juju_model.charmed-chaos.name
}

resource "juju_integration" "litmus-auth-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.auth_app_name
    endpoint = module.charmed-litmus.auth_tls_certificates_endpoint
  }

  application {
    name     = module.self-signed-certificates.app_name
    endpoint = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-backend-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.backend_app_name
    endpoint = module.charmed-litmus.backend_tls_certificates_endpoint
  }

  application {
    name     = module.self-signed-certificates.app_name
    endpoint = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-chaoscenter-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.chaoscenter_app_name
    endpoint = module.charmed-litmus.chaoscenter_tls_certificates_endpoint
  }

  application {
    name     = module.self-signed-certificates.app_name
    endpoint = module.self-signed-certificates.provides.certificates
  }
}

EOF
```

## 2. Apply the changes

Fetch the `self-signed-certificates` module:

```shell
terraform init
```

Apply the new configuration:

```shell
terraform apply -auto-approve
```

When the TLS integration is successfully completed, you will notice a change in the `ChaosCenter` URL printed in the `juju status` output. Namely, it will now indicate an `https` scheme. For example:

```console
Unit                   Workload  Agent  Address       Ports  Message
(...)        
litmus-chaoscenter/0*  active    idle   10.1.194.255         Ready at https://litmus-chaoscenter.charmed-chaos.svc.cluster.local:8185.
(...)
```

## 3. Example of a complete Terraform module including Charmed Litmus plus TLS integration

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
  model    = juju_model.charmed-chaos.name
}

resource "juju_integration" "litmus-auth-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.auth_app_name
    endpoint = module.charmed-litmus.auth_tls_certificates_endpoint
  }

  application {
    name     = module.self-signed-certificates.app_name
    endpoint = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-backend-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.backend_app_name
    endpoint = module.charmed-litmus.backend_tls_certificates_endpoint
  }

  application {
    name     = module.self-signed-certificates.app_name
    endpoint = module.self-signed-certificates.provides.certificates
  }
}

resource "juju_integration" "litmus-chaoscenter-tls" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.chaoscenter_app_name
    endpoint = module.charmed-litmus.chaoscenter_tls_certificates_endpoint
  }

  application {
    name     = module.self-signed-certificates.app_name
    endpoint = module.self-signed-certificates.provides.certificates
  }
}
```

[self-signed-certificates charm]: https://charmhub.io/self-signed-certificates
