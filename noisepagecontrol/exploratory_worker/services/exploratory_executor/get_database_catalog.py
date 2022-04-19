import logging
import subprocess

from django.conf import settings

logger = logging.getLogger("exploratory_worker")


def get_database_catalog(postgres_port, database_name):
    """
    Get database names from postgres cluster
    """

    command = 'sudo -u "%s" "%s" "%s" "%s" "%s"' % (
        settings.POSTGRES_USER,
        settings.GET_DATABASE_CATALOG_SCRIPT,
        postgres_port,
        settings.POSTGRES_USER,
        database_name,
    )

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()

    """
        Result would be somthing like this:
            headers
        -------------------
        catalog ...
        catalog ...
        (2 rows)


    """
    catalog = out.decode("utf-8")
    catalog = "\n".join(catalog.split("\n")[:-3])
    return catalog
