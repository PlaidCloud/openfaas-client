from urllib.parse import urljoin
import re
import time
import simplejson as json
import requests
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from .models.function_definition import FunctionDefinition
from .models.function_list_entry import FunctionListEntry
from .models.api_response import ApiResponse, FunctionNotFoundError

class FaasClient():
    '''Class for interacting with OpenFaaS deployment.
    '''
    _gateway = 'http://gateway.openfaas:8080'
    _deploy_uri = 'system/functions'
    _invoke_uri = 'function/'
    _invoke_async_uri = 'async-function/'
    _get_uri = 'system/function/'
    _scale_uri = 'system/scale-function/'

    def __init__(self, gateway='http://gateway.openfaas:8080'):
        if gateway:
            self._gateway = gateway

    @property
    def gateway_url(self):
        return self._gateway

    @property
    def deploy_url(self):
        return urljoin(self.gateway_url, self._deploy_uri)

    @property
    def invoke_url(self):
        return urljoin(self.gateway_url, self._invoke_uri)

    @property
    def invoke_async_url(self):
        return urljoin(self.gateway_url, self._invoke_async_uri)

    @property
    def get_url(self):
        return urljoin(self.gateway_url, self._get_uri)

    @property
    def scale_url(self):
        return urljoin(self.gateway_url, self._scale_uri)

    def deploy(self, function, asynchronous=True):
        if not isinstance(function, FunctionDefinition):
            raise TypeError('"function" parameter must be of type \
                            FunctionDefinition')
        response = ApiResponse(
            requests.post(self.deploy_url, data=function.serialize()))

        # Super janky synchronous wait
        while not asynchronous:
            try:
                time.sleep(1)
                self.get(function.name)
                break
            except FunctionNotFoundError:
                continue
        return response

    def invoke(self, function_name, params, invoke_async=False, cleanup=False):
        if invoke_async:
            uri = self.invoke_async_url
        else:
            uri = self.invoke_url
        url = urljoin(uri, function_name)
        response = ApiResponse(requests.post(url, data=params))
        if cleanup:
            self.cleanup(response.pod_name)
        return response

    def cleanup(self, pod_name, namespace='openfaas-fn', asynchronous=True):
        config.load_incluster_config()
        kube = client.CoreV1Api()
        kube.delete_namespaced_pod(pod_name, namespace,
                                   client.V1DeleteOptions())
        while not asynchronous:
            try:
                time.sleep(1)
                kube.read_namespaced_pod(name=pod_name,
                                         namespace=namespace)
            except ApiException:
                break

    def delete(self, function_name):
        data = '{{"functionName": "{0}"}}'.format(function_name)
        return requests.delete(self.deploy_url, data=data)

    def delete_all(self, regex=None, asynchronous=False):
        config.load_incluster_config()
        kube = client.CoreV1Api()
        funcs = self.get_all()
        if regex:
            valid = re.compile(regex)
        for name in funcs.keys():
            if regex and valid.match(name):
                self.delete(name)
                while not asynchronous:
                    pod_list = kube.list_namespaced_pod(
                        namespace='openfaas-fn',
                        label_selector='faas_function={}'.format(name))
                    if not pod_list.items:
                        break
                    time.sleep(1)

    def alert(self):
        pass

    def scale_up(self, function_name, replicas):
        func = self.get(function_name)
        return self.scale(function_name, func.replicas + replicas)

    def scale_down(self, function_name, replicas):
        func = self.get(function_name)
        if func.replicas - replicas < 0:
            raise ValueError('Cannot scale below 0 replicas.')
        return self.scale(function_name, func.replicas - replicas)

    def scale(self, function_name, replicas):
        body = dict()
        body['service'] = function_name
        body['replicas'] = replicas
        return ApiResponse(
            requests.post(urljoin(self.scale_url, function_name), json=body))

    def get(self, function_name):
        get_url = urljoin(self.get_url, function_name)
        response = ApiResponse(requests.get(get_url))
        return FunctionListEntry(json.loads(response.text))

    def get_all(self):
        get_url = self.deploy_url
        response = ApiResponse(requests.get(get_url))
        return {func['name']: FunctionListEntry(func) for func \
                in json.loads(response.text)}

    def info(self):
        pass

    def health(self):
        pass
