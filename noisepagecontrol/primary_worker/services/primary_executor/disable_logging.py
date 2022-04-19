import logging
import subprocess
import time

from django.conf import settings

from .get_data_dir import get_data_dir

logger = logging.getLogger("primary_worker")


def disable_logging():
    """
    Disable logging on the primary instance.
    WARNING: Results in a restart
    Script needs to be executed by postgres user
    """

    data_dir = get_data_dir()
    port = settings.PRIMARY_DB_PORT

    command = 'sudo -u "%s" "%s" "%s" "%s" "%s"' % (
        settings.POSTGRES_USER,
        settings.STOP_DATABASE_LOGGING_SCRIPT,
        data_dir,
        port,
        settings.POSTGRES_USER,
    )
    subprocess.call(command, shell=True)
    time.sleep(10)
