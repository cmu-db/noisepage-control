import os 
import subprocess
from pathlib import Path

GET_DATABASE_DATA_DIR_SCRIPT_NAME = "get_database_datadir.sh"
ENABLE_DATABASE_LOGGING_SCRIPT_NAME = "enable_database_logging.sh"
DISABLE_DATABASE_LOGGING_SCRIPT_NAME = "disable_database_logging.sh"

class PrimaryExecutor():

    def __init__(self, scripts_dir, postgres_username, posrgres_port):
        self.SCRIPTS_DIR = scripts_dir
        self.postgres_username = postgres_username
        self.postgres_port = posrgres_port

        # Figure out data dir on start up
        self.data_dir = self.get_data_dir()

    """ Get data dir from database settings """
    def get_data_dir(self):

        command = '"%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / GET_DATABASE_DATA_DIR_SCRIPT_NAME,
            self.postgres_port,
            self.postgres_username,
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


    def start_logging(self):
        """
        Enable logging on the primary instance.
        WARNING: Results in a restart
        Script needs to be executed by postgres user
        """

        command = '"%s" "%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / ENABLE_DATABASE_LOGGING_SCRIPT_NAME,
            self.data_dir,
            self.posrgres_port,
            self.postgres_username,
        )

        subprocess.call(command, shell=True)
        time.sleep(10)

    def stop_logging(self):
        """
        Enable logging on the primary instance.
        WARNING: Results in a restart
        Script needs to be executed by postgres user
        """

        command = '"%s" "%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / DISABLE_DATABASE_LOGGING_SCRIPT_NAME,
            self.data_dir,
            self.posrgres_port,
            self.postgres_username,
        )

        subprocess.call(command, shell=True)
        time.sleep(10)
