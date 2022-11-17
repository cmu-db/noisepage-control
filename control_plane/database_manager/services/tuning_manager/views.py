import json
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from datetime import datetime

from environments.environment import init_environment
from resource_manager.views import get_resource_filepath
from database_manager.types.tuningstatus import TuningStatusType
from database_manager.types.action_status import ActionStatusType
from database_manager.services.workload_manager.views import get_workloads_in_time_range
from database_manager.services.state_manager.views import get_latest_state_before_datetime

logger = logging.getLogger("control_plane")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def tune(request, database_id):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        return tune_database(request, database_id, body["workload_start_time"], body["workload_end_time"])
    elif request.method == "GET":
        return get_tuning_history(request, database_id)


def tune_database(request, database_id, workload_start_time, workload_end_time):
    logger.debug(
        "tune_database for database %s, workload_start_time %s, workload_end_time %s", 
        database_id, workload_start_time, workload_end_time)

    from database_manager.models import Database, TuningInstance
    from resource_manager.models import Resource

    workload_start_time = datetime.strptime(workload_start_time, "%Y-%m-%d_%H%M%S")
    workload_end_time = datetime.strptime(workload_end_time, "%Y-%m-%d_%H%M%S")

    tuning_instance = TuningInstance(
        database_id = database_id,
        workload_start_time = workload_start_time,
        workload_end_time = workload_end_time,
        status = TuningStatusType.RUNNING,
    )
    tuning_instance.save()

    # Get all workload chunks
    workloads = get_workloads_in_time_range(database_id, workload_start_time, workload_end_time)
    print (workloads)

    # Get latest state before workload_start_time
    # TODO: Possible that state does not exist; figure this out

    state = get_latest_state_before_datetime(database_id, workload_start_time)
    print (state)

    # Fetch database and init environment
    # database = Database.objects.get(database_id = database_id)
    # env = init_environment(database)

    # workload = Resource.objects.get(resource_id = workload_id)
    # workload_file_path = get_resource_filepath(workload)

    # state = Resource.objects.get(resource_id = state_id)
    # state_file_path = get_resource_filepath(state)

    # # TODO: Move this to async flow; file transfer can take time
    # callback_url = f"{settings.CONTROL_PLANE_CALLBACK_BASE_URL}/database_manager/tune/tune_database_callback/"
    # env.tune(tuning_instance.tuning_instance_id, workload_file_path, state_file_path, callback_url)

    return HttpResponse("OK")


def get_tuning_history(request, database_id):
    logger.debug("get_tuning_history for database %s", database_id)
    from database_manager.models import TuningInstance
    tuning_instances = list(TuningInstance.objects.filter(database_id=database_id).values())
    return HttpResponse(
        json.dumps(tuning_instances, default=str),
        content_type="application/json"
    )


@csrf_exempt
@require_http_methods(["POST"])
def tune_database_callback(request):
    logger.debug("tune_database_callback")

    from database_manager.models import TuningInstance, TuningAction

    data = json.loads(request.body.decode('utf-8'))
    print (data)

    tuning_instance_id = data["tuning_instance_id"]
    actions = data["actions"]

    tuning_instance = TuningInstance.objects.get(tuning_instance_id = tuning_instance_id)
    tuning_instance.status = TuningStatusType.FINISHED
    tuning_instance.finished_at = datetime.now()
    tuning_instance.save()

    for action in actions:
        new_action = TuningAction(
            database_id = tuning_instance.database_id,
            tuning_instance_id = tuning_instance_id,
            command = action["command"],
            benefit = action["benefit"],
            reboot_required = action["reboot_required"],
            status = ActionStatusType.NOT_APPLIED,
        )
        new_action.save()

        print (new_action)

    
    return HttpResponse("OK")
