# pylint: disable=redefined-outer-name
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
    # Call API method to delete test functions
    api.delete_all(regex='^test-.*$')

@pytest.fixture
def kube():
    config.load_incluster_config()
    return client.CoreV1Api()

def test_invoke_function(capsys, api, kube):
    func = get_func_def()
    func.secrets = ['dockerhub-key']
    # Exception will be thrown if status code >= 400.
    api.deploy(func, asynchronous=False)
    try:
        response = api.invoke(func.name, params='hello')
        with capsys.disabled():
            print("Pod ({}) logs:\n".format(response.pod_name))
            fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)
    except Error as err:
        fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)
        print(err.response.status)
        raise err

def test_invoke_function_with_cleanup(capsys, api, kube):
    func = get_func_def()
    func.secrets = ['dockerhub-key']
    # Exception will be thrown if status code >= 400.
    api.deploy(func, asynchronous=False)
    try:
        # Run 1 should create a test-file file in the pod.
        response1 = api.invoke(func.name, params='hello')
        with capsys.disabled():
            print("Pod #1 ({}) logs:\n".format(response1.pod_name))
            fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)
        api.cleanup(response1.pod_name, FAAS_NAMESPACE, asynchronous=False)

        # Run 2, should create the test-file again. If it doesn't, the
        # pod wasn't killed and restarted between invocations.
        # Logs will indicate if the file already exists.
        response2 = api.invoke(func.name, params='hello')
        with capsys.disabled():
            print("Pod #2 ({}) logs:\n".format(response2.pod_name))
            fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)

        # Pod names would be different if the
        # pod was deleted between invocations.
        assert response1.pod_name != response2.pod_name
    except Error as err:
        fetch_pod_logs(kube, func.name, FAAS_NAMESPACE)
        print(err.response.status)
        raise err

def fetch_pod_logs(kube, name, namespace):
    pod_list = kube.list_namespaced_pod(
        namespace=namespace,
        label_selector='faas_function={}'.format(name))
    print(kube.read_namespaced_pod_log(pod_list.items[0].metadata.name,
                                       namespace))
