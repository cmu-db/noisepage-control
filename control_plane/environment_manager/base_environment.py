from abc import ABC, abstractmethod

class BaseEnvironment(ABC):
    def __init__(self):
        """
        postgres_port: port on which the exploratory postgres is running
        data_dir: directory where collected data will be stored
        config: any config to be passed to the DataCollector
        """
        pass

    @abstractmethod
    def TestConnectivity(self):
        # Tests pem keys work
        # Any other permissions
        pass

    @abstractmethod
    def CollectWorkload(self):
        # Gets a workload and archives it
        pass

    @abstractmethod
    def CollectState(self):
        # Gets state and archives it
        pass

    @abstractmethod
    def CollectMetrics(self):
        # Gets metrics and archives it
        pass

    @abstractmethod
    def Tune(self):
        # Starts tuning
        pass

    @abstractmethod
    def ApplyAction(self):
        # Applies an action
        pass

    @abstractmethod
    def Disconnect(self):
        # Disconnects and tears down any running objects
        pass
