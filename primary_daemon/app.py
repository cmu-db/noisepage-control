from flask import Flask
from pathlib import Path

app = Flask(__name__)

from threading import Lock


from primary_executor import PrimaryExecutor
from resource_manager import create_workload_archive

ROOT_DIR = Path(app.root_path)
SCRIPTS_DIR = ROOT_DIR / "scripts"
RESOURCE_DIR = ROOT_DIR / "resources"

database_executor = PrimaryExecutor(SCRIPTS_DIR, "postgres", "10000")
print (database_executor.data_dir)

log_dir, start, end = database_executor.capture_workload(30)
print (log_dir, start, end)


create_workload_archive(start, end, RESOURCE_DIR, log_dir)

@app.route('/')
def index():
    return 'Hello this is primary worker'

@app.route('/healthcheck')
def healthcheck():
    return 'OK'

