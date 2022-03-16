import os

# TODO: Need to do checks here to prevent double spawning
# TODO: Mark this as a celery task when spawning across machines
def launch_primary_worker(uuid):
    print ("Launching primary for", uuid)
    os.spawnlp(os.P_NOWAIT, 'pipenv', 'pipenv', 'run', './run.sh', 'PRIMARY_WORKER')

