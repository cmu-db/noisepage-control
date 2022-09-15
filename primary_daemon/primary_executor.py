import logging
import subprocess
from pathlib import Path


def get_data_dir():
    """
    Get data dir from database settings
    """

    port = settings.PRIMARY_DB_PORT

    command = '"%s" "%s" "%s"' % (
        settings.GET_DATABASE_DATA_DIR_SCRIPT,
        port,
        settings.POSTGRES_USER,
    )

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()

    """
        Result would be somthing like this:

        setting
        ---------
        /home/kush/db/main/data
        (1 row)

        We need to extract the value
    """
    data_dir = out.decode("utf-8").split("\n")[2].strip()
    return Path(data_dir)
