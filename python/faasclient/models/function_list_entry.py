class FunctionListEntry(object):
    _name = ''
    _image = ''
    _invocation_count = 0
    _replicas = 0
    _available_replicas = 0
    _command = ''
    _labels = []
    _annotations = []

    def __init__(self, response_dict):
        self._name = response_dict['name']
        self._image = response_dict['image']
        self._invocation_count = response_dict['invocationCount']
        self._replicas = response_dict['replicas']
        self._available_replicas = response_dict['availableReplicas']
        self._command = response_dict['envProcess']
        self._labels = response_dict['labels']
        self._annotations = response_dict['annotations']

    @property
    def name(self):
        """The name of the function."""
        return self._name

    @property
    def image(self):
        """The name of the function."""
        return self._image

    @property
    def invocation_count(self):
        """The name of the function."""
        return self._invocation_count

    @property
    def replicas(self):
        """The name of the function."""
        return self._replicas

    @property
    def available_replicas(self):
        """The name of the function."""
        return self._available_replicas

    @property
    def command(self):
        """The name of the function."""
        return self._command

    @property
    def labels(self):
        """The name of the function."""
        return self._labels

    @property
    def annotations(self):
        """The name of the function."""
        return self._annotations
