import logging
import subprocess
import json
from threading import Thread

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings

from .start_exploratory_cluster import start_exploratory_cluster
from .get_data_directory import get_data_directory

logger = logging.getLogger("exploratory_worker")


@csrf_exempt
@require_http_methods(["POST"])
def launch_exploratory_cluster(request):
    data = json.loads(request.body)
    event_name = data["event_name"]
    snapshot = data["snapshot"]

    logger.info(f"Receive launch_exploratory_cluster request: {json.dumps(data)}")

    # asynchronously spins up a pg instance
    thread = Thread(target=start_exploratory_cluster, args=(event_name, snapshot))
    thread.start()

    return HttpResponse()


@csrf_exempt
@require_http_methods(["DELETE"])
def stop_exploratory_cluster(request):
    data = json.loads(request.body)
    port = data["port"]

    logger.info(f"Stopping exploratory Postgres cluster on port {port}...")
    data_dir = get_data_directory(port)
    if data_dir is None:
        return HttpResponseNotFound(f"No exploratory cluster running on port {port}")

    args = [
        "sudo",
        "-u",
        "postgres",
        settings.STOP_EXPLORATORY_CLUSTER_SCRIPT,
        data_dir,
    ]
    subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return HttpResponse()
