from .base_environment import BaseEnvironment

import paramiko
import requests
import json
from io import StringIO

from paramiko.client import SSHClient
from django.conf import settings

from resource_manager.views import get_resource_filepath


def init_client(host, port, user, key_filename):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname = host,
        port = port,
        username = user,
        key_filename = key_filename,
        timeout = 30, 
    )
    return client

class SelfManagedPostgresEnvironment(BaseEnvironment):

    def __init__(self, database):
        self.database = database
        self.config = database.selfmanagedpostgresconfig

    def _init_primary_ssh_client(self):
        return init_client(
            self.config.primary_host,
            int(self.config.primary_ssh_port),
            self.config.primary_ssh_user,
            get_resource_filepath(self.config.primary_ssh_key),
        )

    def _init_replica_ssh_client(self):
        return init_client(
            self.config.replica_host,
            int(self.config.replica_ssh_port),
            self.config.replica_ssh_user,
            get_resource_filepath(self.config.replica_ssh_key),
        )

    def _has_sudo(self, client):
        _, stdout, stderr = client.exec_command("groups")
        stdout=stdout.read()
        stderr=stderr.read()
        client.close()

        if len(stderr) != 0:
            print ("error", error)
            return False

        return b'sudo' in stdout.split()

    def _check_primary_worker_health(self):
        hc_url = "http://%s:%s/healthcheck/" % (
            self.config.primary_host,
            "9000",
        )

        resp = requests.get(hc_url, timeout=5)
        return resp.content == b"OK"

    def _check_replica_worker_health(self):
        hc_url = "http://%s:%s/healthcheck/" % (
            self.config.replica_host,
            "9000",
        )

        resp = requests.get(hc_url, timeout=5)
        return resp.content == b"OK"

    def launch_primary_daemon(self):
        client = self._init_primary_ssh_client()
        sftp = client.open_sftp()
        sftp.put(settings.LAUNCH_PRIMARY_DAEMON_SCRIPT, "launch_primary_daemon.sh")

        _, stdout, stderr = client.exec_command("chmod +x launch_primary_daemon.sh")
        stdout.read()
        stderr=stderr.read()
        if len(stderr):
            client.close()
            return False, "Cannot launch primary daemon\n" + str(stderr)

        # We need to wait out the script's execution; easiset way is to read stdout and stderr
        _, stdout, stderr = client.exec_command("./launch_primary_daemon.sh")
        stdout.read()
        stderr.read()

        client.close()

        if self._check_primary_worker_health():
            return True, ""
        else:
            return False, "Could not start primary daemon"

    def launch_replica_daemon(self):
        client = self._init_replica_ssh_client()
        sftp = client.open_sftp()
        sftp.put(settings.LAUNCH_REPLICA_DAEMON_SCRIPT, "launch_replica_daemon.sh")

        _, stdout, stderr = client.exec_command("chmod +x launch_replica_daemon.sh")
        stdout.read()
        stderr=stderr.read()
        if len(stderr):
            client.close()
            return False, "Cannot launch replica daemon\n" + str(stderr)

        # We need to wait out the script's execution; easiset way is to read stdout and stderr
        _, stdout, stderr = client.exec_command("./launch_replica_daemon.sh")
        stdout.read()
        stderr.read()

        client.close()

        # Do HC
        if self._check_replica_worker_health():
            return True, ""
        else:
            return False, "Could not start replica daemon"


    ######################## BASE METHOD IMPLEMENTATIONS ########################

    def test_connectivity(self):

        # 1. Check sudo permissions on primary
        has_sudo_on_primary = False
        try:
            primary_ssh_client = self._init_primary_ssh_client()
            has_sudo_on_primary = self._has_sudo(primary_ssh_client)
        except Exception as e:
            return False, f"Exception while connecting to primary: {str(e)}"
        finally:
            primary_ssh_client.close()

        if not has_sudo_on_primary:
            return False, "No sudo on primary"

        # 2. Check sudo permissions on replica
        has_sudo_on_replica = False
        try:
            replica_ssh_client = self._init_replica_ssh_client()
            has_sudo_on_replica = self._has_sudo(replica_ssh_client)
        except:
            return False, "Exception while connecting to primary"
        finally:
            replica_ssh_client.close()

        if not has_sudo_on_replica:
            return False, "No sudo on replica"

        return True, ""


    def configure(self):
        # Launch primary daemon
        try:
            launched, err = self.launch_primary_daemon()
            if not launched:
                return False, err
        except Exception as e:
            return False, f"Exception while launching primary daemon: {str(e)}"

        # Launch replica daemon
        try:
            launched, err = self.launch_replica_daemon()
            if not launched:
                return False, err
        except Exception as e:
            return False, f"Exception while launching replica daemon: {str(e)}"

        return True, ""

    def collect_workload(self, num_chunks, callback_url):
        # Gets a workload and archives it
        print ("self managed postgres collecting workoad", num_chunks, resource_id)

        url = "http://%s:%s/collect_workload/" % (
            self.config.primary_host,
            "9000",
        )

        data = {
            "db_name": self.config.db_name,
            "database_id": self.database.database_id,
            "num_chunks": num_chunks,
            "callback_url": callback_url,
        }

        print (url, data)

        headers = {"Content-type": "application/json"}
        requests.post(url, data=json.dumps(data), headers=headers, timeout=3)


    def collect_state(self, resource_id, callback_url):
        # Gets state and archives it
        print ("self managed postgres collecting state", resource_id)

        url = "http://%s:%s/collect_state/" % (
            self.config.primary_host,
            "9000",
        )

        data = {
            "db_name": self.config.db_name,
            "resource_id": resource_id,
            "callback_url": callback_url,
        }

        print (url, data)

        headers = {"Content-type": "application/json"}
        requests.post(url, data=json.dumps(data), headers=headers, timeout=3)
        

    def collect_metrics(self):
        # Gets metrics and archives it
        pass

    def tune(self, tuning_instance_id, workload_file_path, state_file_path, callback_url):
        # Starts tuning
        print ("self managed postgress tune", workload_file_path, state_file_path)

        url = "http://%s:%s/tune/" % (
            self.config.replica_host,
            "9000",
        )

        data = {
            "tuning_instance_id": tuning_instance_id,
            "db_name": self.config.db_name,
            "callback_url": callback_url,
        }

        with StringIO(json.dumps(data)) as data_file, \
            open(workload_file_path, "rb") as wfp, \
            open(state_file_path, "rb") as sfp:

            files = [
                ("workload", ("workload", wfp, "application/x-gtar")),
                ("state", ("state", sfp, "application/x-gtar")),
                ("data", ("data.json", data_file, "application/json")),
            ]

            requests.post(url, files=files, timeout=3)

    def apply_action(self, action_id, command, reboot_required, callback_url):
        url = "http://%s:%s/apply/" % (
            self.config.primary_host,
            "9000",
        )

        data = {
            "db_name": self.config.db_name,
            "action_id": action_id,
            "command": command,
            "reboot_required": reboot_required,
            "callback_url": callback_url,
        }        

        headers = {"Content-type": "application/json"}
        requests.post(url, data=json.dumps(data), headers=headers, timeout=3)

    def disconnect(self):
        # disconnects and tears down any running objects
        pass
