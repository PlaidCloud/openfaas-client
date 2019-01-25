# pylint: disable=redefined-outer-name
import pytest
from faasclient.models.function_definition import FunctionDefinition
from faasclient.models.api_response import ApiResponse, InternalServerError
#from faasclient.models.function_list_entry import FunctionListEntry

def get_func_def():
    return FunctionDefinition(
        name='test-function',
        image_name='openfaas/client-test:latest',
        command='python index.py')

@pytest.fixture
def client():
    from faasclient import FaasClient
    client = FaasClient()
    yield client
    # Call API method to clean up
    client.delete_all(regex='^test-.*$')


def test_deploy_function(client):
    func = get_func_def()
    # Exception will be thrown if status code >= 400.
    response = client.deploy(func)
    assert isinstance(response, ApiResponse), 'Response should be of \
                                              type ApiResponse'

def test_deploy_with_environment_vars(client):
    pass

def test_deploy_function_full(client):
    pass

def test_deploy_duplicate(client):
    func = get_func_def()
    client.deploy(func)
    with pytest.raises(InternalServerError):
        client.deploy(func)
