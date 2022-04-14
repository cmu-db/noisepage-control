import os
import logging

from django.conf import settings

from .resource_types import ResourceType

logger = logging.getLogger("control_plane")


def initialise_workload_resource(tuning_id):
    """
    Creates a resource entry which tracks the workload
    to be collected. This entry would be updated
    in the future when the workload arrives

    Returns: resource_id
    Unique identifier for the inited resource
    """

    from .models import Resource

    workload_resource = Resource(
        tuning_id=tuning_id,
        resource_type=ResourceType.WORKLOAD,
        available=False,
    )
    workload_resource.save()

    return workload_resource.resource_id


def save_workload_resource(tuning_id, resource_id, workload_tar, workload_filename):

    logger.info(
        "Saving worload with resource_id %s tuning_id %s" % (resource_id, tuning_id)
    )

    # Fetch resource entry
    from .models import Resource

    workload_resource = Resource.objects.get(resource_id=resource_id)

    # Make new dir for resource
    resource_dir = settings.RESOURCE_DIR / workload_resource.resource_id
    os.mkdir(resource_dir)

    # Write file to that dir
    with open(resource_dir / workload_filename, "wb") as fp:
        fp.write(workload_tar)

    # Update resource entry
    workload_resource.available = True
    workload_resource.resource_name = workload_filename
    workload_resource.save()
