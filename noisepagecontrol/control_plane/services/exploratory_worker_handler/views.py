import os

# TODO: Need to do checks here to prevent double spawning
# TODO: Mark this as a celery task when spawning across machines
def launch_exploratory_worker(uuid):
    print("Launching exploratory for", uuid)
    os.spawnlp(os.P_NOWAIT, "pipenv", "pipenv", "run", "./run.sh", "EXPLORATORY_WORKER")
