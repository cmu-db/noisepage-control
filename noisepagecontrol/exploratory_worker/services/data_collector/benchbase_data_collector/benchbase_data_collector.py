import logging

from exploratory_worker.services.data_collector.base_data_collector import (
    BaseDataCollector,
)

logger = logging.getLogger("exploratory_worker")


class BenchbaseDataCollector(BaseDataCollector):
    def __init__(self, exp_postgres_port, data_dir, config):
        super().__init__(exp_postgres_port, data_dir, config)

    def setup(self):
        logger.info("Running setup for BenchbaseDataCollector")
        pass

    def collect(self):
        logger.info("Running collect for BenchbaseDataCollector")
        pass

    def cleanup(self):
        logger.info("Running cleanup for BenchbaseDataCollector")
        pass
