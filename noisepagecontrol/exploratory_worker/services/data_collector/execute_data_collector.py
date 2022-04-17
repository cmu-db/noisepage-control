import os
import uuid

from django.conf import settings

from .catalog_data_collector.catalog_data_collector import CatalogDataCollector
from .benchbase_data_collector.benchbase_data_collector import BenchbaseDataCollector

from .data_collector_type import DataCollectorType

DATA_COLLECTOR_MAP = {
    DataCollectorType.CATALOG: CatalogDataCollector,
    DataCollectorType.BENCHBASE: BenchbaseDataCollector,
}

def create_data_dir():
    unique_identifier = str(uuid.uuid4())
    data_dir_path = settings.DATA_COLLECTION_DIR / unique_identifier
    os.mkdir(data_dir_path)
    return data_dir_path

def execute_data_collector(data_collector_type, exp_postgres_port, config):

    # create data dir
    data_dir = create_data_dir()

    # Init appopriate data collector
    # TODO: Handle invalid data collector
    data_collector = DATA_COLLECTOR_MAP[data_collector_type](exp_postgres_port, data_dir, config)

    data_collector.setup()
    data_collector.collect()
    data_collector.cleanup()

    # Transfer back data


