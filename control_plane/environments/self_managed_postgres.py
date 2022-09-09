from .base_environment import BaseEnvironment

import paramiko
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

    def init_primary_ssh_client(self):
        return init_client(
            self.config.primary_host,
            int(self.config.primary_ssh_port),
            self.config.primary_ssh_user,
            get_resource_filepath(self.config.primary_ssh_key),
        )

    def init_replica_ssh_client(self):
        return init_client(
            self.config.replica_host,
            int(self.config.replica_ssh_port),
            self.config.replica_ssh_user,
            get_resource_filepath(self.config.replica_ssh_key),
        )

    def has_sudo(self, client):
        _, stdout, stderr = client.exec_command("groups")
        stdout=stdout.read()
        stderr=stderr.read()
        client.close()

        if len(stderr) != 0:
            print ("error", error)
            return False

        return b'sudo' in stdout.split()

    def launch_primary_daemon(self):
        client = self.init_primary_ssh_client()
        sftp = client.open_sftp()
        sftp.put(settings.LAUNCH_PRIMARY_DAEMON_SCRIPT, "launch_primary_daemon.sh")

        _, _, stderr = client.exec_command("chmod +x launch_primary_daemon.sh")
        stderr=stderr.read()
        if len(stderr):
            return False, "Cannot launch primary daemon\n" + str(stderr)

        print ("starting")
        _, _, stderr = client.exec_command("./launch_primary_daemon.sh")
        stderr=stderr.read()
        if len(stderr):
            return False, "Cannot launch primary daemon\n" + str(stderr)

        print ("done")
        client.close()

        return True, ""

        # Do HC

    def launch_replica_daemon(self):
        client = self.init_replica_ssh_client()
        sftp = client.open_sftp()
        sftp.put(settings.LAUNCH_REPLICA_DAEMON_SCRIPT, "launch_replica_daemon.sh")

        _, _, stderr = client.exec_command("chmod +x launch_replica_daemon.sh")
        stderr=stderr.read()
        if len(stderr):
            return False, "Cannot launch replica daemon\n" + str(stderr)

        _, _, stderr = client.exec_command("./launch_replica_daemon.sh", get_pty = True)
        stderr=stderr.read()
        if len(stderr):
            return False, "Cannot launch replica daemon\n" + str(stderr)

        print ("done")
        client.close()

        # Do HC

        return True, ""

    def test_connectivity(self):

        # 1. Check sudo permissions on primary
        has_sudo_on_primary = False
        # try:
        primary_ssh_client = self.init_primary_ssh_client()
        has_sudo_on_primary = self.has_sudo(primary_ssh_client)
        primary_ssh_client.close()
        # except:
        #     pass

        if not has_sudo_on_primary:
            return False, "No sudo on primary"

        # 2. Check sudo permissions on replica
        has_sudo_on_replica = False
        try:
            replica_ssh_client = self.init_replica_ssh_client()
            has_sudo_on_replica = self.has_sudo(replica_ssh_client)
            replica_ssh_client.close()
        except:
            pass

        if not has_sudo_on_replica:
            return False, "No sudo on replica"

        return True, ""


    def configure(self):
        # Launch daemons
        print ("launching primary")
        launched, err = self.launch_primary_daemon()
        if not launched:
            print ("returning ", launched)
            return False, err

        print ("launching replica")
        launched, err = self.launch_replica_daemon()
        if not launched:
            return False, err

        return True, ""

    def collect_workload(self):
        # Gets a workload and archives it
        pass

    def collect_state(self):
        # Gets state and archives it
        pass

    def collect_metrics(self):
        # Gets metrics and archives it
        pass

    def tune(self):
        # Starts tuning
        pass

    def apply_action(self):
        # Applies an action
        pass

    def disconnect(self):
        # disconnects and tears down any running objects
        pass
