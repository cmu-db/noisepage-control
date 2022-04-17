import json
import logging
import subprocess

from django.conf import settings
import requests

from .get_data_directory import get_data_directory

logger = logging.getLogger("exploratory_worker")


def start_exploratory_postgres(event_name, snapshot):
    # TODO Tim: probe an available port from 20000 instead of hard-coding
    exploratory_postgres_port = 20000

    logger.info(
        f"starting exploratory Postgres cluster on port {exploratory_postgres_port}..."
    )

    args = [
        "sudo",
        "-u",
        settings.POSTGRES_USER,
        settings.START_EXPLORATORY_POSTGRES_SCRIPT,
        str(exploratory_postgres_port),
    ]
    if snapshot:
        logger.info("taking snapshot from replica cluster...")
        replica_dir = get_data_directory(settings.REPLICA_DB_PORT)
        args += ["-r", replica_dir]
    try:
        res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # TODO Tim: should send fail message back to control plane instead of sending nothing?
    except OSError:
        logger.error(
            f"Error while executing {settings.START_EXPLORATORY_POSTGRES_SCRIPT}"
        )
        return
    if res.returncode != 0:
        logger.error(f"{settings.START_EXPLORATORY_POSTGRES_SCRIPT} returncode != 0")
        logger.error(res.stdout.decode("utf-8"))
        logger.error(res.stderr.decode("utf-8"))
        return

    logger.info("done!")

    # Send back exploratory cluster port to control plane
    control_plane_url = settings.CONTROL_PLANE_URL
    control_plane_port = settings.CONTROL_PLANE_PORT
    tuning_id = settings.TUNING_ID

    url = (
        "http://%s:%s/exploratory_worker_handler/launch_exploratory_postgres_callback/"
        % (
            control_plane_url,
            control_plane_port,
        )
    )

    data = {
        "tuning_id": tuning_id,
        "event_name": event_name,
        "exploratory_postgres_port": exploratory_postgres_port,
    }
    logger.info(f"Sending {json.dumps(data)} back to control plane")

    headers = {"Content-type": "application/json"}
    requests.post(url, data=json.dumps(data), headers=headers)
