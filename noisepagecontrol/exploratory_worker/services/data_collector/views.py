import logging
import json
from threading import Thread

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .execute_data_collector import execute_data_collector

logger = logging.getLogger("exploratory_worker")


@csrf_exempt
@require_http_methods(["POST"])
def collect_data(request):

    data = json.loads(request.body)

    event_name = data["event_name"]
    resource_id = data["resource_id"]

    config = data["config"]
    postgres_port = data["postgres_port"]
    data_collector_type = data["data_collector_type"]

    thread = Thread(
        target=execute_data_collector,
        args=(
            event_name,
            resource_id,
            data_collector_type,
            postgres_port,
            config,
        ),
    )
    thread.start()

    return HttpResponse("OK")
