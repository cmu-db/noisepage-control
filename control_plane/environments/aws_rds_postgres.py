from .base_environment import BaseEnvironment

class AWSRDSPostgresEnvironment(BaseEnvironment):

    def test_connectivity(self):
        # Tests pem keys work
        # Any other permissions
        print ("testing connectivity aws rds", self.database)
        pass

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
