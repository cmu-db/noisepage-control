import logging
import os
import shutil

from django.conf import settings

logger = logging.getLogger("exploratory_worker")


def create_data_archive(data_dir):

    file_name = os.path.basename(data_dir)
    data_base_dir = settings.DATA_COLLECTION_DIR

    shutil.make_archive(data_dir, "gztar", data_base_dir, file_name)
    archive_path = str(data_base_dir / file_name) + ".tar.gz"
    logger.info("Created archive %s" % (archive_path))
    return archive_path
