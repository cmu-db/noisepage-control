import os
import uuid

from django.conf import settings

from .benchbase_data_collector.benchbase_data_collector import (
    BenchbaseDataCollector,
)
from .catalog_data_collector.catalog_data_collector import CatalogDataCollector
from .create_data_archive import create_data_archive
from .data_collector_type import DataCollectorType
from .transfer_data import transfer_data

DATA_COLLECTOR_MAP = {
    DataCollectorType.CATALOG: CatalogDataCollector,
    DataCollectorType.BENCHBASE: BenchbaseDataCollector,
}


def create_data_dir():
    unique_identifier = str(uuid.uuid4())
    data_dir_path = settings.DATA_COLLECTION_DIR / unique_identifier
    os.mkdir(data_dir_path)
    return data_dir_path


def execute_data_collector(
    event_name, resource_id, data_collector_type, postgres_port, config
):

    # create data dir
    data_dir = create_data_dir()

    # Init appopriate data collector
    # TODO: Handle invalid data collector
    data_collector = DATA_COLLECTOR_MAP[data_collector_type](
        postgres_port, data_dir, config
    )

    data_collector.setup()
    data_collector.collect()
    data_collector.cleanup()

    # Create data archive
    data_archive_path = create_data_archive(data_dir)

    # Transfer back data
    transfer_data(event_name, resource_id, data_archive_path)
