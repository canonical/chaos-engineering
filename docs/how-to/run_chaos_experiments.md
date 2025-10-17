# Run Chaos experiments with Charmed Litmus

In this how-to guide we will conduct a simple Chaos Experiment simulating POD deletion to check if the System Under Test
can recover from such fault. To achieve this, we will bootstrap Chaos Infrastructure onto a Kubernetes cluster, 
define a Resilience Probe and create and run the experiment.

### Pre-requisites:

- a Charmed Chaos Engineering platform deployed on your Kubernetes cluster (see the [Getting started tutorial])
- kubectl 

## 1. Deploy System Under Test (SUT)

In this guide we will use the [self-signed-certificates] charm as a SUT.

Create a Juju model for the `self-signed-certificates` charm:

```shell
juju add-model certs
```

Deploy the charm:

```shell
juju deploy self-signed-certificates
```

Monitor the status of the deployment:

```console
juju status --relations --watch 1s
```

The deployment is ready when the `self-signed-certificates` charm is in the `active/idle` state.

## 2. Bootstrap Chaos Infrastructure

In the Litmus Portal navigate to the `Environments` tab and click on the `+ New Environment` button.<br>
In the pop-up window fill in the name of the environment and select the environment type.

In this guide we will create an environment of type `Production` and we will call it `getting-started`:

```{image} ../images/litmus_create_env.png
:alt: Create Litmus environment
:align: center
```

Confirm configuration by clicking the `Save` button.

To bootstrap Chaos Infrastructure onto a Kubernetes cluster click on the newly created environment and then click
the `+ Enable Chaos` button.

First, provide a name for the infrastructure. In this guide we will use `self-signed-certificates-test`:

```{image} ../images/bootstrap_infra_step_1.png
:align: center
```

Next, choose the Infrastructure type, specify the Kubernetes namespace to deploy the Infrastructure to and define
a Service Account responsible for managing the Infrastructure.

In this guide we will deploy the namespace-specific Chaos Infrastructure along the SUT (note the `Installation
Location` being the same as the name of the Juju model we deployed `self-signed-certificates` to):

```{image} ../images/bootstrap_infra_step_2.png
:align: center
```

Last, follow the instructions from points 2 and 3 of the `Kubernetes Setup Instructions` :

```{image} ../images/bootstrap_infra_step_3.png
:align: center
```

After applying the manifests click the `Done` button.

Deploying Chaos Infrastructure should take approximately 3-5 minutes. Successful deployment will be indicated
by the Infrastructure status turned into `CONNECTED`:

```{image} ../images/bootstrap_infra_success.png
:align: center
```

## 3. Define a Resilience Probe

In the Litmus Portal navigate to the `Resilience Probes` menu and click the `+ New Probe` button.<br>
Select the probe of type `Command` and configure it using the values below:

- Name:                `pod-up-probe`
- Timeout:             `10s`
- Interval:            `1s`
- Attempt:             `1`
- Command:             `kubectl -n certs get pods | grep self-signed-certificates | grep Running | wc -l`
- Type:                `int`
- Comparison Criteria: `>`
- Value:               `0`

Correctly configured probe should look as show below:

```{image} ../images/litmus_probe_config.png
:align: center
```

## 3. Create a Chaos Experiment

In the Litmus Portal navigate to the `Chaos Experiments` menu and click the `+ New Experiment` button.

Name the test and select a Chaos Infrastructure to use:

```{image} ../images/experiment_step_1.png
:align: center
```

Start off building an experiment using `Blank Canvas`.

In the `Experiment Builder` click the `Add` button and add the `pod-delete` fault:

```{image} ../images/experiment_step_2.png
:align: center
```

Configure the fault with the following values:

- App Kind:      `statefulset`
- App Namespace: `certs`
- App Label:     `app.kubernetes.io/name=self-signed-certificates`

```{image} ../images/experiment_step_3.png
:align: center
```

In the `Probes` tab select previously created `pod-up-probe` and confirm your choice by clicking the `Add to Fault` button.
Select the `End of Test (EOT)` probe execution mode and apply changes.

At this point you experiment should look similar to the one presented below:

```{image} ../images/experiment_step_4.png
:align: center
```

Save your changes by clicking the `Save` button in the top-right corner of the screen.

## 3. Run a Chaos Experiment

Click the `Run` button in the top-right corner of the screen to run the Chaos Experiment:

```{image} ../images/experiment_run.png
:align: center
```

Running the experiment should take approximately 3 minutes.

When the experiment state changes from `RUNNING` to `COMPLETED` the run is done and the result is presented:

```{image} ../images/experiment_success.png
:align: center
```

[Getting started tutorial]: ./../tutorial/getting_started.md
[self-signed-certificates]: https://charmhub.io/self-signed-certificates
