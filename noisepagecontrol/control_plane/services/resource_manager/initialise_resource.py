import logging

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

    logging.info(
        "Initialised new resource %s for tuning id %s"
        % (resource.resource_id, tuning_id)
    )
    return resource.resource_id
