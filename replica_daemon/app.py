from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello this is replica worker'

@app.route('/healthcheck')
def index():
    return 'OK'
