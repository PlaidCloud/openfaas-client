class ApiResponse():
    _status_code = 0
    _reason = ''
    _text = ''

    def __init__(self, response):
        self._status_code = response.status_code
        self._reason = response.reason
        self._text = response.text
        self._pod_name = response.headers.get('Pod-Name')

        if self.status_code >= 400:
            self.raise_http_error()

    @property
    def status(self):
        return "{0} {1}: {2}".format(self.status_code,
                                     self.reason,
                                     self.text)

    @property
    def status_code(self):
        return self._status_code

    @property
    def reason(self):
        return self._reason

    @property
    def text(self):
        return self._text

    @property
    def pod_name(self):
        return self._pod_name

    def raise_http_error(self):
        switch = {
            400: BadRequestError,
            404: FunctionNotFoundError,
            500: InternalServerError,
        }
        exception = switch.get(self.status_code, Error)
        raise exception(self)

class Error(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, response):
        try:
            # Python 3 syntax
            super().__init__(response.status)
        except:
            # Python 2 syntax
            super(Exception, self).__init__(response.status)
        self.response = response
        # self.message = response.status

class FunctionNotFoundError(Error):
    """Raised when no function is deployed under given name."""

class BadRequestError(Error):
    """Raised when OpenFaaS API returns a 400 error."""

class InternalServerError(Error):
    """Raised when OpenFaaS API returns a 500 error."""
