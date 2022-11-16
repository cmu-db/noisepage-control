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
GET_DATABASE_DATA_DUMP_TAR_SCRIPT = "get_database_data_dump_tar.sh"


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

    """ Get data dump (tar) for a given database"""
    def get_database_data_dump_tar(self, database_name):
        command = '"%s" "%s" "%s" "%s" ' % (
            self.SCRIPTS_DIR / GET_DATABASE_DATA_DUMP_TAR_SCRIPT,
            self.postgres_port,
            self.postgres_username,
            database_name
        )

        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        dump_tar, err = process.communicate()
        return dump_tar

    """
    Enable logging on the database.
    WARNING: Results in a restart
    Script needs to be executed by postgres user
    """
    def enable_logging(self):

        command = '"%s" "%s" "%s" "%s" "%s"' % (
            self.SCRIPTS_DIR / ENABLE_DATABASE_LOGGING_SCRIPT_NAME,
            self.data_dir,
            self.postgres_port,
            self.postgres_username,
            str(5) # log rotation age in minutes
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
