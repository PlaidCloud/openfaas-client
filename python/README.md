# OpenFaaS Python Client
This package was written with the intended use case of interacting with (faas-netes)[https://github.com/openfaas/faas-netes].

# Development Dependencies
Building and running unit tests requires the following:
- [docker](https://docs.docker.com/install/])
- [minikube](https://github.com/kubernetes/minikube/releases)
- [skaffold](https://github.com/GoogleContainerTools/skaffold/releases)
- [faas-netes](https://github.com/openfaas/faas-netes/tree/master/chart/openfaas) (see notes below on installation)

The client currently assumes the OpenFaaS function namespace is `openfaas-fn`. Because of this, you'll need to do one of two things:
1. Specify the [function namespace](https://github.com/openfaas/faas-netes/blob/master/chart/openfaas/values.yaml#L1) as `openfaas-fn` prior to deploying the helm chart.
2. Edit the unit tests locally. 
  
The unit tests run from a pod in the `default` namespace, which interacts with pods directly in the

# Installation
    git clone https://github.com/gbates101/openfaas-client.git
    cd openfaas-client/python
    python setup.py install

# Running Tests
    cd openfaas-client/python
    bash build_test_fixtures.sh
    skaffold dev