# Running Haystack Pipeline on Kubernetes using KubeRay

## Overview

In this example we will run a simple pipeline with [Ray on Kubernetes](https://docs.ray.io/en/latest/cluster/kubernetes/index.html). Our goal is to setup a basic RayCluster on your local machine and then start the pipeline. During the experiment we will see that some things needs to be considered when pipeline is submitted to a remote environment. Most of the examples usually run locally, but in this case we will see some steps to take into account before we run pipeline in a remote Ray setup. Specifically, remote nodes (e.g. pods in k8s) do not know what dependencies should be pre-installed or what environment variables needs to be set. As you might have guessed, in a production environment you need to carefully plan how things are configured, e.g.:

- Ensure dependencies are pre-installed as part of containers (e.g. `haystack-ai` package as well as `ray-haystack`)
- Environment variables are set on remote nodes (pods)
- Workload is properly managed by requesting enough cluster resources (CPUs, GPUs, RAM)
- etc

We are not aiming here to provide a production ready setup, but rather focus on simple use case - to demonstrate that it is possible to connect to existing KubeRay cluster and run the pipeline.

## Project structure

```shell
.
├── README.md
├── pipeline.py # Sample Haystack (Ray) Pipeline
├── requirements.txt # Dependencies you will need to install, providing same version of Ray as it will be used in k8s
└── runtime_env.yaml # Runtime Environment definition with environment variables and dependencies required
```

> **Note**
> The code for sample is a modified version of the [Generating Structured Output with Loop-Based Auto-Correction](https://haystack.deepset.ai/tutorials/28_structured_output_with_loop) tutorial. So you will need OpenAI API Key to run the example.

## Install Dependencies

The `requirements.txt` declares project's dependencies. In our case we must make sure the version of `ray` library installed will match the version of Ray which will be installed in RayCluster in its workers (k8s pods).

```shell
ray[default]==2.34.0 # ray[default] will also install Ray dashboard
ray-haystack
```

Install dependencies by running:

```shell

```

## Setup RayCluster

We will setup a cluster using KubeRay operator. For that we will follow the steps from this [tutorial](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html).

### Step 1: Create a Kubernetes cluster

On my local I am using Docket Desktop with Kubernetes already enabled. You could use [kind](https://kind.sigs.k8s.io/) as suggested in the tutorial.

### Step 2: Deploy a KubeRay operator

```shell
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update

# Install both CRDs and KubeRay operator v1.2.1.
helm install kuberay-operator kuberay/kuberay-operator --version 1.2.1

# Confirm that the operator is running in the namespace `default`.
kubectl get pods
# NAME                                READY   STATUS    RESTARTS   AGE
# kuberay-operator-7fbdbf8c89-pt8bk   1/1     Running   0          27s
```

> **Note**
> We are using version 1.2.1 of the helm chart (in tutorial version is 1.1.1).

```bash
helm install kuberay-operator kuberay/kuberay-operator --version 1.2.1

helm install raycluster kuberay/ray-cluster --version 1.2.1 \
    --set worker.replicas=2 \
    --set worker.resources.limits.memory="2G" \
    --set worker.resources.requests.memory="2G"
```
