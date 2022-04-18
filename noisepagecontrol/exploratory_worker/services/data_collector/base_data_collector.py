from abc import ABC, abstractmethod


class BaseDataCollector(ABC):
    def __init__(self, postgres_port, data_dir, config):
        """
        postgres_port: port on which the exploratory postgres is running
        data_dir: directory where collected data will be stored
        config: any config to be passed to the DataCollector
        """

        self.postgres_port = postgres_port
        self.data_dir = data_dir
        self.config = config

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def collect(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass
