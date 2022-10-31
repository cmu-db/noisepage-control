from .base_environment import BaseEnvironment

class AWSRDSPostgresEnvironment(BaseEnvironment):

    def test_connectivity(self):
        # Tests pem keys work
        # Any other permissions
        print ("testing connectivity aws rds", self.database)
        pass

    def collect_workload(self, time_period, resource_id, callback_url):
        # Gets a workload and archives it
        pass

    def collect_state(self, resource_id, callback_url):
        # Gets state and archives it
        pass

    def collect_metrics(self):
        # Gets metrics and archives it
        pass

    def tune(self, workload_file_path, state_file_path, callback_url):
        # Starts tuning
        pass

    def def apply_action(self, action_id, command, reboot_required, callback_url)::
        # Applies an action
        pass

    def disconnect(self):
        # disconnects and tears down any running objects
        pass
