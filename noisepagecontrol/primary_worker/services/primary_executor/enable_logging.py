import time
import logging
import subprocess

from django.conf import settings

from .get_data_dir import get_data_dir

logger = logging.getLogger("exploratory_worker")


def enable_logging():
    """
    Enable logging on the primary instance.
    WARNING: Results in a restart
    Script needs to be execited by postgres user
    """

    data_dir = get_data_dir()
    port = settings.PRIMARY_DB_PORT
    pg_username = settings.PRIMARY_DB_USERNAME

    command = 'sudo -u "%s" "%s" "%s" "%s" "%s"' % (
        settings.POSTGRES_USER,
        settings.START_DATABASE_LOGGING_SCRIPT,
        data_dir,
        port,
        pg_username,
    )
    subprocess.call(command, shell=True)
    time.sleep(10)
