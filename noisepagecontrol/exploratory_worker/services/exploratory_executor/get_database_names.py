import logging
import subprocess

from django.conf import settings

logger = logging.getLogger("exploratory_worker")


def get_database_names(postgres_port):
    """
    Get database names from postgres cluster
    """

    port = postgres_port
    pg_username = "kushagrasingh"

    command = 'sudo -u "%s" "%s" "%s" "%s"' % (
        pg_username,
        settings.GET_DATABASE_NAMES_SCRIPT,
        port,
        pg_username,
    )

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()

    """
        Result would be somthing like this:
            datname      
        -------------------
        postgres
        noisepage_control
        (2 rows)


        We need to extract the value
    """

    database_names = list(map(
        lambda db_name: db_name.strip(), 
        out.decode("utf-8").split("\n")[2:-3]
    ))

    return database_names
