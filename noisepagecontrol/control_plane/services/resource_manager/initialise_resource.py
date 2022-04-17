import os
import logging

from django.conf import settings

logger = logging.getLogger("control_plane")


def initialise_resource(tuning_id, resource_type):
    """
    Creates a resource entry which tracks the workload
    to be collected. This entry would be updated
    in the future when the workload arrives

    Returns: resource_id
    Unique identifier for the inited resource
    """

    from .models import Resource

    resource = Resource(
        tuning_id=tuning_id,
        resource_type=resource_type,
        available=False,
    )
    resource.save()

    # Make new dir for resource
    resource_dir = settings.RESOURCE_DIR / resource.resource_id
    os.mkdir(resource_dir)

    return resource.resource_id
