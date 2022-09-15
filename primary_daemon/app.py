from flask import Flask
from pathlib import Path

app = Flask(__name__)

from threading import Lock


from primary_executor import PrimaryExecutor

ROOT_DIR = Path(app.root_path)
SCRIPTS_DIR = ROOT_DIR / "scripts"

database_executor = PrimaryExecutor(SCRIPTS_DIR, "postgres", "10000")

@app.route('/')
def index():
    return 'Hello this is primary worker'

@app.route('/healthcheck')
def healthcheck():
    return 'OK'

