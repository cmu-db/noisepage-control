import os
import logging

from constants import (
    TUNING_ID_ENV_VAR_KEY,
    CONTROL_PLANE_URL_ENV_KEY,
    CONTROL_PLANE_PORT_ENV_KEY,
    LAUNCH_EVENT_NAME_ENV_VAR_KEY,
    REPLICA_DB_PORT_ENV_VAR_KEY,
    REPLICA_DB_USERNAME_ENV_VAR_KEY,
)

logger = logging.getLogger("control_plane")

# TODO: Need to do checks here to prevent double spawning
# TODO: Mark this as a celery task when spawning across machines
def launch_exploratory_worker(
    tuning_id, replica_db_port, replica_db_username, event_name
):
    logger.info(
        "Launching exploratory worker. Tuning id: %s Event name: %s"
        % (tuning_id, event_name)
    )

    # Very hacky way of passing env vars and launching
    # Needs to be reworked when we move workers away from local
    os.spawnvpe(
        os.P_NOWAIT,
        "pipenv",
        ["pipenv", "run", "./run.sh", "EXPLORATORY_WORKER"],
        env={
            **os.environ,
            TUNING_ID_ENV_VAR_KEY: tuning_id,
            CONTROL_PLANE_URL_ENV_KEY: "127.0.0.1",
            CONTROL_PLANE_PORT_ENV_KEY: "8000",
            LAUNCH_EVENT_NAME_ENV_VAR_KEY: event_name,
            REPLICA_DB_PORT_ENV_VAR_KEY: replica_db_port,
            REPLICA_DB_USERNAME_ENV_VAR_KEY: replica_db_username,
        },
    )
