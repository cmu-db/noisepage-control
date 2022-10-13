import json
import logging
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

logger = logging.getLogger("control_plane")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def actions(request, database_id):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        return generate_action(request, database_id, body["workload_id"], body["state_id"])
    elif request.method == "GET":
        return get_actions(request, database_id)


def generate_action(request, database_id, workload_id, state_id):
    logger.debug("generate_action for database %s, workload %s, state %s", database_id, workload_id, state_id)
    # TODO: Implement this
    return HttpResponse("OK")


def get_actions(request, database_id):
    logger.debug("get_actions for database %s", database_id)
    from database_manager.models import Action
    actions = list(Action.objects.filter(database_id=database_id).values())
    return HttpResponse(
        json.dumps(actions),
        content_type="application/json"
    )


@csrf_exempt
@require_http_methods(["POST"])
def generate_action_callback(request):
    logger.debug("generate_action_callback")
    # TODO: Implement this


@csrf_exempt
@require_http_methods(["GET"])
def download_action(request, action_id):
    logger.debug("download_action")
    # TODO: Implement this
    # from resource_manager.models import Resource
    # workload = Resource.objects.get(resource_id = workload_id)

    # if workload.available == False:
    #     return HttpResponse("File not available")

    # filepath = get_resource_filepath(workload)
    # print (filepath)
    
    # fp = open(filepath, "rb")
    # response = FileResponse(fp)

    # response['Content-Type'] = "application/gzip"
    # return response
