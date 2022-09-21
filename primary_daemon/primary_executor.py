import os 
import time
import subprocess

from pathlib import Path
from threading import Lock
from datetime import datetime



GET_DATABASE_DATA_DIR_SCRIPT_NAME = "get_database_data_dir.sh"
GET_DATABASE_LOGGING_DIR_SCRIPT = "get_database_logging_dir.sh"
ENABLE_DATABASE_LOGGING_SCRIPT_NAME = "enable_database_logging.sh"
DISABLE_DATABASE_LOGGING_SCRIPT_NAME = "disable_database_logging.sh"

GET_DATABASE_NAMES_SCRIPT = "get_database_names.sh"


class PrimaryExecutor():

    def __init__(self, scripts_dir, postgres_username, posrgres_port):
        self.SCRIPTS_DIR = scripts_dir
        self.postgres_username = postgres_username
        self.postgres_port = posrgres_port
        
        self.WORKLOAD_CAPTURE_MUTEX = Lock()

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


    """ Get logging dir from database settings """
    def get_logging_dir(self):
        
        command = '"%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / GET_DATABASE_LOGGING_DIR_SCRIPT,
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
            log
            (1 row)

            We need to extract the value
        """
        log_dir = out.decode("utf-8").split("\n")[2].strip()

        return self.data_dir / log_dir

    """ Get logging dir from database settings """
    def get_database_names(self):
        
        command = '"%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / GET_DATABASE_NAMES_SCRIPT,
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
            log
            (1 row)

            We need to extract the value
        """
        database_names = list(
            map(lambda db_name: db_name.strip(), out.decode("utf-8").split("\n")[2:-3])
        )

        return database_names


    """
    Enable logging on the database.
    WARNING: Results in a restart
    Script needs to be executed by postgres user
    """
    def enable_logging(self):

        command = '"%s" "%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / ENABLE_DATABASE_LOGGING_SCRIPT_NAME,
            self.data_dir,
            self.postgres_port,
            self.postgres_username,
        )

        subprocess.call(command, shell=True)
        time.sleep(5)


    """
    Disable logging on the database.
    WARNING: Results in a restart
    Script needs to be executed by postgres user
    """
    def disable_logging(self):

        command = '"%s" "%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / DISABLE_DATABASE_LOGGING_SCRIPT_NAME,
            self.data_dir,
            self.postgres_port,
            self.postgres_username,
        )

        subprocess.call(command, shell=True)
        time.sleep(5)




    """
    This method captures the workload on a primary instance.
    Only allow one concurrent capture;
    synchronised via `WORKLOAD_CAPTURE_MUTEX`
    """
    def capture_workload(self, time_period):

        self.WORKLOAD_CAPTURE_MUTEX.acquire()

        try:
            # Enable logging
            self.enable_logging()
            print ("Enabled logging")

            # Wait for time_period seconds
            capture_start_time = datetime.now()
            for it in range(0, time_period, 5):
                time.sleep(5)
                print ("Captured %d seconds" % (it + 5))
            capture_end_time = datetime.now()

            # Disable logging
            self.disable_logging()
            print ("Disabled logging")

            # Create workload archive
            # archive_path = create_workload_archive(capture_start_time, capture_end_time)

            # Transfer archive to control plane
            # transfer_workload(archive_path, command_name, resource_id)

        finally:
            self.WORKLOAD_CAPTURE_MUTEX.release()


        return self.get_logging_dir(), capture_start_time, capture_end_time