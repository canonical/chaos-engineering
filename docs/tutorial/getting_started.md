# Getting started

In this tutorial, we will deploy and run the Charmed Chaos Engineering platform using Juju and Terraform.

To complete this tutorial, you will need a machine which meets the following requirements:

- 8GB of RAM
- 50GB of free disk space
- An Ubuntu (or another operating system which supports [snapd]) environment to run the commands

## 1. Install Canonical K8s

From your terminal, install Canonical K8s and bootstrap it:

```shell
sudo snap install k8s --classic --channel=1.33-classic/stable
cat << EOF | sudo k8s bootstrap --file -
containerd-base-dir: /opt/containerd
disable-rbac: true
cluster-config:
  network:
    enabled: true
  dns:
    enabled: true
  local-storage:
    enabled: true
EOF
```

## 2. Bootstrap a Juju controller

From your terminal, install Juju.

```shell
sudo snap install juju --channel=3.6/stable
```

Save the K8s credentials, we will need them later to bootstrap the Juju controller.

```shell
mkdir -p ~/.kube
sudo k8s config > ~/.kube/config
mkdir -p ~/.local/share/juju/
sudo k8s config > ~/.local/share/juju/credentials.yaml
```

Bootstrap a Juju controller

```shell
juju bootstrap k8s
```

## 3. Install Terraform

From your terminal, install Terraform.

```shell
sudo snap install terraform --classic
```

## 4. Deploy the Charmed Chaos Engineering platform

On the host machine create a new directory called `terraform`:

```shell
mkdir terraform
```

Inside the newly created `terraform` directory create a `versions.tf` file:

```shell
cd terraform
cat << EOF > versions.tf
terraform {
  required_providers {
    juju = {
      source  = "juju/juju"
      version = ">= 0.14.0"
    }
  }
}
EOF
```

Create a new Terraform module:

```shell
cat << EOF > main.tf
resource "juju_model" "charmed-chaos" {
  name = "charmed-chaos"
}

module "charmed-litmus" {
  source = "git::https://github.com/canonical/litmus-operators//terraform"

  model      = juju_model.charmed-chaos.name
  depends_on = [juju_model.charmed-chaos]
}
EOF
```

```{note}
You can get a ready example by cloning [this Git repository](https://github.com/canonical/chaos-engineering).
All necessary files are in the `examples/terraform/getting_started` directory.
```

Initialize the Juju Terraform provider:

```shell
terraform init
```

Apply your Terraform configuration:

```shell
terraform apply -auto-approve
```

<!--
This hidden block is here for documentation testing purposes and will not be rendered in the official documentation.
```shell
uv run --with jubilant python -c "import jubilant as j; j.Juju(model='charmed-chaos').wait(j.all_active, timeout=600)"
```
-->

The deployment process should take approximately 5-10 minutes.

Monitor the status of the deployment:

```console
juju switch charmed-chaos
juju status --relations --watch 1s
```

The deployment is ready when all the charms are in the `active/idle` state.

Example:

```console
ubuntu@host:~/terraform $ juju status
Model              Controller                  Cloud/Region                Version  SLA          Timestamp
charmed-chaos      k8s                         k8s                         3.6.9    unsupported  12:25:15+02:00

App                 Version  Status  Scale  Charm                   Channel   Rev  Address         Exposed  Message
litmus-auth                  active      1  litmus-auth-k8s         2/edge      5  10.152.183.92   no       
litmus-backend               active      1  litmus-backend-k8s      2/edge      5  10.152.183.186  no       
litmus-chaoscenter           active      1  litmus-chaoscenter-k8s  2/edge     11  10.152.183.102  no       Ready at http://litmus-chaoscenter.charmed-chaos.svc.cluster.local:8185.
mongodb-k8s         6.0.24   active      3  mongodb-k8s             6/stable   81  10.152.183.175  no       

Unit                   Workload  Agent  Address       Ports  Message
litmus-auth/0*         active    idle   10.1.194.219         
litmus-backend/0*      active    idle   10.1.194.231         
litmus-chaoscenter/0*  active    idle   10.1.194.255         Ready at http://litmus-chaoscenter.charmed-chaos.svc.cluster.local:8185.
mongodb-k8s/0*         active    idle   10.1.194.214         
mongodb-k8s/1          active    idle   10.1.194.198         
mongodb-k8s/2          active    idle   10.1.194.230         

Integration provider           Requirer                             Interface                Type     Message
litmus-auth:http-api           litmus-chaoscenter:auth-http-api     litmus_auth_http_api     regular  
litmus-auth:litmus-auth        litmus-backend:litmus-auth           litmus_auth              regular  
litmus-backend:http-api        litmus-chaoscenter:backend-http-api  litmus_backend_http_api  regular  
mongodb-k8s:database           litmus-auth:database                 mongodb_client           regular  
mongodb-k8s:database           litmus-backend:database              mongodb_client           regular  
mongodb-k8s:database-peers     mongodb-k8s:database-peers           mongodb-peers            peer     
mongodb-k8s:ldap-peers         mongodb-k8s:ldap-peers               ldap-peers               peer     
mongodb-k8s:status-peers       mongodb-k8s:status-peers             status-peers             peer     
mongodb-k8s:upgrade-version-a  mongodb-k8s:upgrade-version-a        upgrade                  peer
```

## 5. Log in to the Litmus ChaosCenter

Retrieve the `chaoscenter/0` unit IP address from the `juju status` output. In the example above, this is `10.1.194.255`; yours will likely differ.

In your browser navigate to `http://{CHAOSCENTER_IP}:8185`. You should see the Litmus login page:

```{image} ../images/litmus_login_screen.png
:alt: Litmus login screen
:align: center
```

Use the default credentials (username `admin`, password `litmus`) to log in to the Litmus ChaosCenter for the first time. 
The first time you log in you will be prompted to change the default password. Make sure to store it in a safe place.

```{note}
Litmus stores all user credentials in the database. This means that once you changed your `admin` password, it will not be reset 
to the default one unless you re-deploy the database. Redeploying Litmus alone will not affect your passwords.
```

After you successfully logged in, you should see the Litmus admin panel:

```{image} ../images/litmus_admin_panel.png
:alt: Litmus admin panel
:align: center
```

Congratulations!<br>
You have reached the end of this tutorial. For more information about the Charmed Chaos Engineering platform please see our other documents.

## 6. Destroy the environment

Destroy the Terraform deployment:

```shell
terraform destroy -auto-approve
```

```{note}
Terraform does not remove anything from the working directory. If needed, please clean up the `terraform` directory manually.
```

Destroy the Juju controller and all its models:

```shell
juju kill-controller k8s --no-prompt
```

[snapd]: https://snapcraft.io/docs
