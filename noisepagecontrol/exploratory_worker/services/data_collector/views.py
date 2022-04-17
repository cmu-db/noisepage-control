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


    config = data["config"]
    exp_postgres_port = data["exp_postgres_port"]
    data_collector_type = data["data_collector_type"]

    execute_data_collector(
        data_collector_type, exp_postgres_port, config)

    return HttpResponse("OK")
