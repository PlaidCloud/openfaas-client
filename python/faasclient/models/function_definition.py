import string
import simplejson as json

class Del:
    # pylint: disable=too-few-public-methods
    """Creates a mapping of digits for translating strings"""
    def __init__(self, keep=string.digits):
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)


def _strip_letters(text):
    digits = Del()
    return text.translate(digits)


class FunctionDefinition():
    # pylint: disable=too-many-instance-attributes
    _request_params = {}

    def __init__(self, name, image_name, command, response_body=None):
        self.name = name
        self.image_name = image_name
        self.command = command

        if isinstance(response_body, dict):
            self._request_params = response_body


    @property
    def name(self):
        """The name of the function."""
        return self._request_params['service']

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._request_params['service'] = name

    @property
    def image_name(self):
        """The docker image used by the deployed function."""
        return self._request_params['image']

    @image_name.setter
    def image_name(self, image_name):
        if isinstance(image_name, str):
            self._request_params['image'] = image_name

    @property
    def command(self):
        """The command to run inside the deployed function ."""
        return self._request_params['envProcess']

    @command.setter
    def command(self, command):
        if isinstance(command, str):
            self._request_params['envProcess'] = command

    @property
    def environment_variables(self):
        return self._request_params['envVars']

    @environment_variables.setter
    def environment_variables(self, environment_variables):
        self._request_params['envVars'] = environment_variables

    @property
    def constraints(self):
        return self._request_params['envVars']

    @constraints.setter
    def constraints(self, constraints):
        self._request_params['constraints'] = constraints

    @property
    def labels(self):
        return self._request_params['labels']

    @labels.setter
    def labels(self, labels):
        self._request_params['labels'] = labels

    @property
    def annotations(self):
        return self._request_params['annotations']

    @annotations.setter
    def annotations(self, annotations):
        self._request_params['annotations'] = annotations

    @property
    def secrets(self):
        return self._request_params['secrets']

    @secrets.setter
    def secrets(self, secrets):
        self._request_params['secrets'] = secrets

    @property
    def cpu_limit(self):
        '''The upper-limit of CPUs to allocate, expressed as a float. Can be
        partial values. Must be greater than or equal to cpu_request'''
        limits = self._request_params.get('limits', {})
        if limits and limits['cpu']:
            return float(limits.get('cpu'))
        return None

    @cpu_limit.setter
    def cpu_limit(self, cpu_limit):
        '''The upper-limit of CPUs to allocate, expressed as a float. Can be
        partial values. Must be greater than or equal to cpu_request'''
        limit = "{0:.2f}".format(round(cpu_limit, 2))
        if 'limits' in self._request_params:
            self._request_params['limits']['cpu'] = limit
        else:
            self._request_params['limits'] = {'cpu': limit}

    @property
    def cpu_request(self):
        '''The number of CPUs to request, expressed as a float. Can be
        partial values. Must be less or equal to cpu_limit.'''
        requests = self._request_params.get('requests', {})
        if requests and requests['cpu']:
            return float(requests.get('cpu'))
        return None

    @cpu_request.setter
    def cpu_request(self, cpu_request):
        '''The number of CPUs to request, expressed as a float. Can be
        partial values. Must be less or equal to cpu_limit.'''
        request = "{0:.2f}".format(round(cpu_request, 2))
        if 'requests' in self._request_params:
            self._request_params['requests']['cpu'] = request
        else:
            self._request_params['requests'] = {'cpu': request}

    @property
    def memory_limit(self):
        '''Upper-limit of memory (megabytes) to allocate, expressed as an int.
        Must be greater than or equal to memory_request.'''
        limits = self._request_params.get('limits', {})
        if limits and limits['memory']:
            return float(_strip_letters(limits.get('memory')))
        return None

    @memory_limit.setter
    def memory_limit(self, memory_limit):
        '''Upper-limit of memory (megabytes) to allocate, expressed as an int.
        Must be greater than or equal to memory_request.'''
        limit = "{0}M".format(memory_limit)
        if 'limits' in self._request_params:
            self._request_params['limits']['memory'] = limit
        else:
            self._request_params['limits'] = {'memory': limit}

    @property
    def memory_request(self):
        '''Total megabytes of memory to request, expressed as an int. Must be
        less or equal to memory_limit.'''
        requests = self._request_params.get('requests', {})
        if requests and requests['memory']:
            return float(_strip_letters(requests.get('memory')))
        return None

    @memory_request.setter
    def memory_request(self, memory_request):
        '''Total megabytes of memory to request, expressed as an int. Must be
        less or equal to memory_limit.'''
        request = "{0}M".format(memory_request)
        if 'requests' in self._request_params:
            self._request_params['requests']['memory'] = request
        else:
            self._request_params['requests'] = {'memory': request}

    def serialize(self):
        return json.dumps(self._request_params, sort_keys=True, indent=4 * ' ')
