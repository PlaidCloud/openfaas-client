#!/usr/bin/env python
# coding=utf-8
"""
    Contacting the OpenFaaS Gateway requires a docker secret to be created in openfaas namespace:
    - basic-auth

    which requires two data points:
    - basic-auth-user
    - basic-auth-password

    Creating a docker-registry secret:
    kubectl -n openfaas-fn patch serviceaccount default -p '{"imagePullSecrets": [{"name": "dockerhub-key"}]}'
    https://docs.openfaas.com/deployment/kubernetes/#option-2-link-an-image-pull-secret-to-the-namespaces-serviceaccount

    Probably want an imagePullPolicy of IfNotPresent:
    https://docs.openfaas.com/deployment/kubernetes/#set-a-custom-imagepullpolicy
"""
from .api import FaasClient