import uuid

from django.db import models

def tuningInstance_state_default():
    return { }
    
def autogenerate_uuid():
    return str(uuid.uuid4())

# Create your models here.
class TuningInstance(models.Model):

    primary_url = models.CharField(max_length = 30)
    primary_port = models.CharField(max_length = 5)
    replica_url = models.CharField(max_length = 30)
    replica_port = models.CharField(max_length = 5)

    # Unique identifier for this tuning request
    uuid = models.CharField(max_length = 36, primary_key = True, default = autogenerate_uuid)
    state = models.JSONField("state", default = tuningInstance_state_default)
