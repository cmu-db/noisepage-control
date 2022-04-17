from django.contrib import admin

# Import models from various services
from control_plane.services.tuning_manager.models import TuningInstance, TuningEvent
from control_plane.services.resource_manager.models import Resource
from control_plane.services.exploratory_worker_handler.models import ExploratoryPGInfo

# Register for visibility in admin
admin.site.register(TuningInstance)
admin.site.register(TuningEvent)
admin.site.register(Resource)
admin.site.register(ExploratoryPGInfo)
