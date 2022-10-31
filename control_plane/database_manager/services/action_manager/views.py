import json
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core import serializers

from database_manager.types.action_status import ActionStatusType

from environments.environment import init_environment

logger = logging.getLogger("control_plane")

@csrf_exempt
@require_http_methods(["GET"])
def get_actions(request, database_id):

    # get actions for datbase_id
    from database_manager.models import TuningAction

    tuning_instance_id = request.GET["tuning_instance_id"]

    # # Mock data
    # new_action = TuningAction(
    #     database_id = 1,
    #     tuning_instance_id = 1,
    #     command = "CREATE UNIQUE INDEX title_idx ON films (title);",
    #     benefit = 200.0,
    #     reboot_required = False,
    #     status = ActionStatusType.NOT_APPLIED,
    # )
    # new_action.save()
    # new_action = TuningAction(
    #     database_id = 1,
    #     tuning_instance_id = 1,
    #     command = "ALTER SYSTEM SET max_connections TO '20';",
    #     benefit = 100.0,
    #     reboot_required = False,
    #     status = ActionStatusType.NOT_APPLIED,
    # )
    # new_action.save()

    
    actions = list(TuningAction.objects.filter(
        database_id=database_id,
        tuning_instance_id=tuning_instance_id,
    ).values())

    return HttpResponse(
        json.dumps(actions),
        content_type="application/json"
    )


@csrf_exempt
@require_http_methods(["GET"])
def apply_action(request, tuning_action_id):

    from database_manager.models import TuningAction
    from database_manager.models import Database

    tuning_action = TuningAction.objects.get(tuning_action_id = tuning_action_id)

    # Get database env
    database_id = tuning_action.database_id
    database = Database.objects.get(database_id = database_id)
    env = init_environment(database)

    callback_url = \
        f"{settings.CONTROL_PLANE_CALLBACK_BASE_URL}" + \
        "/database_manager/action/apply_action_callback/"

    # Apply action
    env.apply_action(
        tuning_action.tuning_action_id,
        tuning_action.command,
        tuning_action.reboot_required, 
        callback_url
    )

    # TODO: Potential race if callback comes back; not likely
    tuning_action.status = TuningStatusType.APPLYING
    tuning_action.save()

    return HttpResponse(
        serializers.serialize("json", [tuning_action]),
        content_type="application/json"
    )

def apply_action_callback(request):
    return HttpResponse("action callback")