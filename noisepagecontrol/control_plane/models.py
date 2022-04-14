from django.contrib import admin

# Import models from various services
from control_plane.services.tuning_manager.models import TuningInstance, TuningEvent
from control_plane.services.resource_manager.models import Resource

# Register for visibility in admin 
admin.site.register(TuningInstance)
admin.site.register(TuningEvent)
admin.site.register(Resource)
