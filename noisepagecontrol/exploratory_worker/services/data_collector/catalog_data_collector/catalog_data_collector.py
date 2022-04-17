import logging

from exploratory_worker.services.data_collector.base_data_collector import (
    BaseDataCollector,
)
from exploratory_worker.services.exploratory_executor.get_database_names import (
    get_database_names,
)
from exploratory_worker.services.exploratory_executor.get_database_catalog import (
    get_database_catalog,
)

logger = logging.getLogger("exploratory_worker")


class CatalogDataCollector(BaseDataCollector):
    def __init__(self, postgres_port, data_dir, config):
        super().__init__(postgres_port, data_dir, config)

    def setup(self):
        logger.info("Running setup for CatalogDataCollector")

        # Get list of databases
        self.database_names = get_database_names(self.postgres_port)
        logger.info("Database names: %s" % (str(self.database_names)))

    def collect(self):
        logger.info("Running collect for CatalogDataCollector")

        # Get catalog for each database and write to file
        for database_name in self.database_names:
            database_catalog = get_database_catalog(self.postgres_port, database_name)

            catalog_file_name = database_name + ".catalog"

            with open(self.data_dir / catalog_file_name, "w") as fp:
                fp.write(database_catalog)

    def cleanup(self):
        logger.info("Running cleanup for CatalogDataCollector")
        pass
