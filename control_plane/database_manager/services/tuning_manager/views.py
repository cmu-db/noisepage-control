import json
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger("control_plane")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def tune(request, database_id):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        return tune_database(request, database_id, body["workload_id"], body["state_id"])
    elif request.method == "GET":
        return get_tuning_history(request, database_id)


def tune_database(request, database_id, workload_id, state_id):
    logger.debug("tune_database for database %s, workload %s, state %s", database_id, workload_id, state_id)
    # TODO: Implement this
    return HttpResponse("OK")


def get_tuning_history(request, database_id):
    logger.debug("get_tuning_history for database %s", database_id)
    from database_manager.models import TuningInstance
    tuning_instances = list(TuningInstance.objects.filter(database_id=database_id).values())
    return HttpResponse(
        json.dumps(tuning_instances),
        content_type="application/json"
    )


@csrf_exempt
@require_http_methods(["POST"])
def tune_database_callback(request):
    logger.debug("tune_database_callback")
    # TODO: Implement this

