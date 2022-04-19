from control_plane.services.exploratory_worker_handler.models import (
    ExploratoryPGInfo,
)
from control_plane.services.resource_manager.models import Resource

# Import models from various services
from control_plane.services.tuning_manager.models import (
    TuningCommand,
    TuningInstance,
)
from django.contrib import admin

# Register for visibility in admin
admin.site.register(TuningInstance)
admin.site.register(TuningCommand)
admin.site.register(Resource)
admin.site.register(ExploratoryPGInfo)
