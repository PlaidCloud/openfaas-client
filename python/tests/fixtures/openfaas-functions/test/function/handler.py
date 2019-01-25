import os

def handle(app, request):
    if os.path.isfile('test-file'):
        app.logger.info('file already exists')
    else:
        app.logger.info('creating test-file')
        touch('test-file')
    app.logger.info('request data: {}'.format(str(request)))
    return ('', 204)

def touch(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)
