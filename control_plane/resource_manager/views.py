import logging
import os

from django.conf import settings

from .resource_type import ResourceType

logger = logging.getLogger("control_plane")

def initialise_resource_dir(database_id):
    """
    Creates a resource entry which tracks the workload
    to be collected. This entry would be updated
    in the future when the workload arrives

    Returns: resource_id
    Unique identifier for the inited resource
    """

    # Init new resource dir for database
    resource_dir = settings.RESOURCE_DIR / database_id
    os.mkdir(resource_dir)
    
    logging.info(
        "Initialised new resource dir for database id %s"
        % (database_id)
    )

def initialise_resource(database_id, resource_type):
    """
    Creates a resource entry which tracks the workload
    to be collected. This entry would be updated
    in the future when the workload arrives

    Returns: resource_id
    Unique identifier for the inited resource
    """

    from .models import Resource

    resource = Resource(
        database_id=database_id,
        resource_type=resource_type,
        available=False,
    )
    resource.save()

    
    logging.info(
        "Initialised new resource %s for tuning id %s"
        % (resource.resource_id, database_id)
    )
    return resource.resource_id


def save_resource(resource_id, resource_file, resource_filename):

    # Fetch resource entry
    from .models import Resource

    resource = Resource.objects.get(resource_id=resource_id)

    logger.info(
        "Saving resource with id %s for database %s" % (resource_id, resource.database_id)
    )

    # Make new dir for resource
    resource_dir = settings.RESOURCE_DIR / resource.database_id / resource_id
    os.mkdir(resource_dir)

    # Write file to resource dir
    with open(resource_dir / resource_filename, "wb") as fp:
        fp.write(resource_file)

    # If key, set appropriate permissions
    if resource.resource_type == ResourceType.KEY:
        os.chmod(resource_dir / resource_filename, 0o400)

    # Update resource entry
    resource.available = True
    resource.resource_name = resource_filename
    resource.save()

    return resource

def get_resource_filepath(resource):
    return str(settings.RESOURCE_DIR / resource.database_id / resource.resource_id / resource.resource_name)
