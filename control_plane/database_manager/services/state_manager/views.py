import json 

from django.http import HttpResponse, FileResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from resource_manager.views import initialise_resource, save_resource, get_resource_filepath
from resource_manager.resource_type import ResourceType

from environments.environment import init_environment

@csrf_exempt
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        return collect_state(request)
    return HttpResponse("Hello, world. This is state manager")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def states(request, database_id):
    if request.method == "POST":
        collect_state(database_id)
        return HttpResponse("OK")

    elif request.method == "GET":
        return get_states(request, database_id)


def get_states(request, database_id):
    # get states with database_id
    from resource_manager.models import Resource
    states = list(Resource.objects.filter(database_id=database_id, resource_type=ResourceType.STATE).values())
    return HttpResponse(
        json.dumps(states, default=str),
        content_type="application/json"
    )


def collect_state(database_id):

    from database_manager.models import Database

    # Fetch database and init environment
    database = Database.objects.get(database_id = database_id)
    env = init_environment(database)

    callback_url = f"{settings.CONTROL_PLANE_CALLBACK_BASE_URL}/database_manager/state/collect_state_callback/"
    env.collect_state(callback_url)
    

@csrf_exempt
@require_http_methods(["POST"])
def collect_state_callback(request):

    data = json.loads(request.FILES["data"].read().decode("utf-8"))
    database_id = data["database_id"]
    collected_at = data["collected_at"]
    print("Received collected state data. Database id: %s" % (database_id))

    # Save
    captured_tar = request.FILES["state"].read()
    file_name = "%s_%s.tar.gz" % (database_id, collected_at)
    friendly_name = file_name
    
    resource_id = initialise_resource(
        database_id, ResourceType.STATE, friendly_name)
    save_resource(
        resource_id, captured_tar, file_name, 
        collected_at = datetime.datetime.strptime(collected_at, "%Y-%m-%d_%H%M%S"))

    return HttpResponse("OK")

@csrf_exempt
@require_http_methods(["GET"])
def download_state(request, state_id):

    from resource_manager.models import Resource
    state = Resource.objects.get(resource_id = state_id)

    if state.available == False:
        return HttpResponse("File not available")

    filepath = get_resource_filepath(state)
    print (filepath)
    
    fp = open(filepath, "rb")
    response = FileResponse(fp)

    response['Content-Type'] = "application/gzip"
    return response

