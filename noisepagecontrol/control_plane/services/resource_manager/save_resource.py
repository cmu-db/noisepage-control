import logging

from django.conf import settings

logger = logging.getLogger("control_plane")


def save_resource(tuning_id, resource_id, resource_tar, resource_filename):

    logger.info(
        "Saving worload with resource_id %s tuning_id %s" % (resource_id, tuning_id)
    )

    # Fetch resource entry
    from .models import Resource

    resource = Resource.objects.get(resource_id=resource_id)

    resource_dir = settings.RESOURCE_DIR / resource.resource_id

    # Write file to resource dir
    with open(resource_dir / resource_filename, "wb") as fp:
        fp.write(resource_tar)

    # Update resource entry
    resource.available = True
    resource.resource_name = resource_filename
    resource.save()
