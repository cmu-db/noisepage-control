import logging
import subprocess

from django.conf import settings

logger = logging.getLogger("exploratory_worker")

def start_exploratory_cluster(snapshot):
    # TODO Tim: probe an available port from 10000 instead of hard-coding
    exploratory_cluster_port = 10000

    logger.info(f"starting exploratory Postgres cluster on port {exploratory_cluster_port}...")

    args = ['sudo', '-u', 'postgres', settings.START_EXPLORATORY_CLUSTER_SCRIPT, str(exploratory_cluster_port)]
    if snapshot:
        logger.info("taking snapshot from replica cluster...")
        args.append('-s')
    try:
        res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        logger.error(f"Error while executing {settings.START_EXPLORATORY_CLUSTER_SCRIPT}")
        return
    if res.returncode != 0:
        logger.error(f"{settings.START_EXPLORATORY_CLUSTER_SCRIPT} returncode != 0")
        logger.error(res.stdout.decode('utf-8'))
        logger.error(res.stderr.decode('utf-8'))
        return
    
    logger.info("done!")

    # TODO Tim: send back the port to control plane
    logger.info(f"TODO: send exploratory_cluster_port: {exploratory_cluster_port} back to control plane!!!")
