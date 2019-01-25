# pylint: disable=redefined-outer-name
import time
import pytest
from kubernetes import client, config
from faasclient.models.function_definition import FunctionDefinition
from faasclient.models.api_response import Error
#from faasclient.models.function_list_entry import FunctionListEntry

FAAS_NAMESPACE = 'openfaas-fn'

def get_func_def():
    return FunctionDefinition(
        name='test-function',
        image_name='openfaas/client-test:latest',
        command='python index.py')

@pytest.fixture
def api():
    from faasclient import FaasClient
    api = FaasClient()
    yield api
    # Call API method to clean up
    api.delete_all(regex='^test-.*$')

@pytest.fixture
def kube():
    config.load_incluster_config()
    return client.CoreV1Api()

def test_scale_function(api, kube):
    func = get_func_def()
    func.secrets = ['dockerhub-key']
    # Exception will be thrown if status code >= 400.
    api.deploy(func, asynchronous=False)
    try:
        # Test initial conditions.
        response = api.get(func.name)
        pod_count = get_pod_count(kube, func.name, FAAS_NAMESPACE)
        assert pod_count == response.replicas
        assert pod_count == 1

        # Scale the function.
        api.scale(func.name, 3)
        time.sleep(10)

        # Retest conditions for change.
        response = api.get(func.name)
        pod_count = get_pod_count(kube, func.name, FAAS_NAMESPACE)
        assert pod_count == response.replicas
        assert pod_count == 3

        # Scale the function once more.
        api.scale(func.name, 2)

        # We must give kubernetes some time to terminate pods.
        # Ideally we would be polling the api server until pods are gone.
        wait_for_termination(kube, func.name, FAAS_NAMESPACE, 2)

        # Retest conditions one more time.
        response = api.get(func.name)
        assert response.replicas == 2
    except Error as err:
        fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)
        print(err.response.status)
        raise err

def test_scale_up_function(api, kube):
    func = get_func_def()
    func.secrets = ['dockerhub-key']
    # Exception will be thrown if status code >= 400.
    api.deploy(func, asynchronous=False)
    try:
        # Test initial conditions.
        response = api.get(func.name)
        pod_count = get_pod_count(kube, func.name, FAAS_NAMESPACE)
        assert pod_count == response.replicas
        assert pod_count == 1

        # Scale the function by adding one pod
        api.scale_up(func.name, 1)

        # Give kubernetes some time to get the new pod running.
        time.sleep(10)

        # Retest conditions for change.
        response = api.get(func.name)
        pod_count = get_pod_count(kube, func.name, FAAS_NAMESPACE)
        assert pod_count == response.replicas
        assert pod_count == 2
    except Error as err:
        fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)
        print(err.response.status)
        raise err

def test_scale_down_function(api, kube):
    func = get_func_def()
    func.secrets = ['dockerhub-key']
    # Exception will be thrown if status code >= 400.
    api.deploy(func, asynchronous=False)
    try:
        # Test initial conditions.
        response = api.get(func.name)
        pod_count = get_pod_count(kube, func.name, FAAS_NAMESPACE)
        assert pod_count == response.replicas
        assert pod_count == 1

        # Scale the function badly by hitting negative pods.
        with pytest.raises(ValueError):
            api.scale_down(func.name, 3)

        # Scale again, but this time with valid input (scaling to 0)
        api.scale_down(func.name, 1)

        # We must wait for kubernetes to terminate pods.
        wait_for_termination(kube, func.name, FAAS_NAMESPACE, 0)

        # Retest conditions for change.
        response = api.get(func.name)
        assert response.replicas == 0
    except Error as err:
        fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)
        print(err.response.status)
        raise err

def wait_for_termination(kube, name, namespace, desired_replicas):
    retry = 30
    while get_pod_count(kube, name, namespace) > desired_replicas:
        if retry == 0:
            raise TimeoutError("Timeout expired waiting \
                                for pods to terminate.")
        retry -= 1
        time.sleep(1)

def get_pod_count(kube, name, namespace):
    pod_list = kube.list_namespaced_pod(
        namespace=namespace,
        label_selector='faas_function={}'.format(name))
    return len(pod_list.items)

def fetch_pod_logs(kube, name, namespace):
    pod_list = kube.list_namespaced_pod(
        namespace=namespace,
        label_selector='faas_function={}'.format(name))
    print(kube.read_namespaced_pod_log(pod_list.items[0].metadata.name,
                                       namespace))
