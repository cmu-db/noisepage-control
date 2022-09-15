from flask import Flask

app = Flask(__name__)

from threading import Lock


"""
    Lock to prevent multiple concurrent workload captures
"""
WORKLOAD_CAPTURE_MUTEX = Lock()


@app.route('/')
def index():
    return 'Hello this is primary worker'

@app.route('/healthcheck')
def healthcheck():
    return 'OK'

