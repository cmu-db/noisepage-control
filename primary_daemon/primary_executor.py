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
EXECUTE_COMMAND_SCRIPT_NAME = "execute_command.sh"

GET_DATABASE_NAMES_SCRIPT = "get_database_names.sh"
GET_DATABASE_CATALOG_SCRIPT = "get_database_catalog.sh"
GET_DATABASE_INDEX_SCRIPT = "get_database_index.sh"
GET_DATABASE_DDL_DUMP_SCRIPT = "get_database_ddl_dump.sh"
GET_DATABASE_DATA_DUMP_SCRIPT = "get_database_data_dump.sh"


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

    """ Get all database names """
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

    """ Get catalog for a given database """
    def get_database_catalog(self, database_name):

        command = '"%s" "%s" "%s" "%s" ' % (
            self.SCRIPTS_DIR / GET_DATABASE_CATALOG_SCRIPT,
            self.postgres_port,
            self.postgres_username,
            database_name
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

    """ Get indexes for a given database """
    def get_database_index(self, database_name):

        command = '"%s" "%s" "%s" "%s" ' % (
            self.SCRIPTS_DIR / GET_DATABASE_INDEX_SCRIPT,
            self.postgres_port,
            self.postgres_username,
            database_name
        )

        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = process.communicate()

        """
            Result would be somthing like this:
                headers
            -------------------
            index ...
            index ...
            (2 rows)


        """
        indexes = out.decode("utf-8")
        indexes = "\n".join(indexes.split("\n")[:-3])
        return indexes

    """ Get ddl dump for a given database"""
    def get_database_ddl_dump(self, database_name):

        command = '"%s" "%s" "%s" "%s" ' % (
            self.SCRIPTS_DIR / GET_DATABASE_DDL_DUMP_SCRIPT,
            self.postgres_port,
            self.postgres_username,
            database_name
        )

        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = process.communicate()

        ddl = out.decode("utf-8")
        return ddl

    """ Get data dump for a given database"""
    def get_database_data_dump(self, database_name):
        # TODO: Implement this
        # Use "pg_dump -U username -p port -F t database_name > data_dump.tar"
        # to get the data dump
        pass

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


    """
    This method captures the workload on a primary instance.
    Only allow one concurrent capture;
    synchronised via `WORKLOAD_CAPTURE_MUTEX`
    """
    def apply_action(self, cmd, reboot_required, database_name):

        
        if reboot_required:
            reboot_required = 1
        else:
            reboot_required = 0

        command = '"%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / EXECUTE_COMMAND_SCRIPT_NAME,
            cmd,
            self.data_dir,
            int(reboot_required),
            self.postgres_port,
            self.postgres_username,
            database_name)
        subprocess.call(command, shell=True)
