import os
import json
import logging
from io import StringIO
from datetime import datetime
from threading import Thread, Lock

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .capture_workload import capture_workload

logger = logging.getLogger("primary_worker")


@csrf_exempt
@require_http_methods(["POST"])
def start_workload_capture(request):

    data = json.loads(request.body)

    event_name = data["event_name"]
    resource_id = data["resource_id"]
    time_period = data["time_period"]

    # Start capture on a new thread
    thread = Thread(
        target=capture_workload, args=(time_period, event_name, resource_id)
    )
    thread.start()

    # Current thread responds 200 OK
    # TODO: What happens when workload capture fails?
    return HttpResponse("OK")
