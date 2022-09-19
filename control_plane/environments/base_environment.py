from abc import ABC, abstractmethod

class BaseEnvironment(ABC):
    def __init__(self, database):
        self.database = database

        """
        postgres_port: port on which the exploratory postgres is running
        data_dir: directory where collected data will be stored
        config: any config to be passed to the DataCollector
        """
        pass

    @abstractmethod
    def test_connectivity(self):
        # Tests pem keys work
        # Any other permissions
        pass

    @abstractmethod
    def configure(self):
        # Launch daemons etc.
        pass

    @abstractmethod
    def collect_workload(self, time_period, resource_id, callback_url):
        # Gets a workload and archives it
        pass

    @abstractmethod
    def collect_state(self):
        # Gets state and archives it
        pass

    @abstractmethod
    def collect_metrics(self):
        # Gets metrics and archives it
        pass

    @abstractmethod
    def tune(self):
        # Starts tuning
        pass

    @abstractmethod
    def apply_action(self):
        # Applies an action
        pass

    @abstractmethod
    def disconnect(self):
        # disconnects and tears down any running objects
        pass
