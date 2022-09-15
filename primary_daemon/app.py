from flask import Flask
from pathlib import Path

app = Flask(__name__)

from threading import Lock


from primary_executor import PrimaryExecutor

ROOT_DIR = Path(app.root_path)
SCRIPTS_DIR = ROOT_DIR / "scripts"

database_executor = PrimaryExecutor(SCRIPTS_DIR, "postgres", "10000")
print (database_executor.data_dir)

database_executor.enable_logging()
print (database_executor.get_logging_dir())
database_executor.disable_logging()

@app.route('/')
def index():
    return 'Hello this is primary worker'

@app.route('/healthcheck')
def healthcheck():
    return 'OK'

