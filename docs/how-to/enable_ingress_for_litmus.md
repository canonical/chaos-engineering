# Enable ingress for Charmed Litmus

This how-to guide outlines the process of enabling ingress for Charmed Litmus.<br>
Enabling ingress can be done as both Day 1 and Day 2 operation.

In this how-to we will use the [Traefik Kubernetes Charmed Operator] as an ingress controller.

To complete this guide, your Kubernetes cluster will need a LoadBalancer with at least 1 available IP address.

## 1. Add Traefik to your Charmed Chaos Engineering platform Terraform module

```{note}
In this guide it is assumed that the Terraform module responsible for deploying the Charmed Litmus is named `charmed-litmus`.
If you use different name, please make sure to update the code below.
```

Update your solution Terraform module (here it's named `main.tf`):

```shell
cat << EOF >> main.tf
module "traefik" {
  source  = "git::https://github.com/canonical/traefik-k8s-operator//terraform"
  model   = juju_model.charmed-chaos.name
  channel = "latest/stable"
}

resource "juju_integration" "litmus-chaoscenter-traefik" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.chaoscenter_app_name
    endpoint = module.charmed-litmus.chaoscenter_ingress_endpoint
  }

  application {
    name     = module.traefik.app_name
    endpoint = module.traefik.endpoints.traefik_route
  }
}

EOF
```

## 2. Apply the changes

Fetch the `traefik` module:

```shell
terraform init
```

Apply new configuration:

```shell
terraform apply -auto-approve
```

Successful integration is indicated by the change of the `ChaosCenter` URL printed in `juju status` output. 
New address of the `ChaosCenter` should point to the IP address at which Traefik is served. Example:

```console
Unit                   Workload  Agent  Address       Ports  Message
(...)        
litmus-chaoscenter/0*  active    idle   10.1.194.214         Ready at http://10.0.0.3:8185.
(...)
traefik/0*             active    idle   10.1.194.236         Serving at 10.0.0.3
```

## 3. Example of a complete solution Terraform module including Charmed Litmus integrated with Traefik

```console
resource "juju_model" "charmed-chaos" {
  name = "charmed-chaos"
}

module "charmed-litmus" {
  source = "git::https://github.com/canonical/litmus-operators//terraform"

  model      = juju_model.charmed-chaos.name
  depends_on = [juju_model.charmed-chaos]
}

module "traefik" {
  source  = "git::https://github.com/canonical/traefik-k8s-operator//terraform"
  model   = juju_model.charmed-chaos.name
  channel = "latest/stable"
}

resource "juju_integration" "litmus-chaoscenter-traefik" {
  model = juju_model.charmed-chaos.name

  application {
    name     = module.charmed-litmus.chaoscenter_app_name
    endpoint = module.charmed-litmus.chaoscenter_ingress_endpoint
  }

  application {
    name     = module.traefik.app_name
    endpoint = module.traefik.endpoints.traefik_route
  }
}
```

[Traefik Kubernetes Charmed Operator]: https://github.com/canonical/traefik-k8s-operator
