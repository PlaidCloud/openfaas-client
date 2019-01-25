# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import os
import logging
from flask import Flask, request
from function import handler
#from gevent.wsgi import WSGIServer
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True

@app.after_request
def add_pod_name_header(response):
    response.headers.add('Pod-Name', os.environ['HOSTNAME'])
    return response

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def main_route(path):
    ret = handler.handle(app, request.get_data())
    return ret

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=False)

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
