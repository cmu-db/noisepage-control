import logging
import subprocess

from django.conf import settings

from .get_data_dir import get_data_dir

logger = logging.getLogger("primary_worker")


def get_logging_dir():
    """
    Get logging dir from database settings
    """

    port = settings.PRIMARY_DB_PORT
    pg_username = settings.PRIMARY_DB_USERNAME

    command = '"%s" "%s" "%s"' % (
        settings.GET_DATABASE_LOGGING_DIR_SCRIPT,
        port,
        pg_username,
    )

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()

    """
        Result would be somthing like this:
        
        setting 
        ---------
        log
        (1 row)

        We need to extract the value
    """
    log_dir = out.decode("utf-8").split("\n")[2].strip()
    data_dir = get_data_dir()

    return data_dir / log_dir
