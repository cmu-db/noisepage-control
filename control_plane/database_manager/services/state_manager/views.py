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
        data = json.loads(request.body.decode("utf-8"))
        return collect_state(request, database_id, data["friendly_name"])
    elif request.method == "GET":
        return get_states(request, database_id)


def get_states(request, database_id):
    # get states with database_id
    from resource_manager.models import Resource
    states = list(Resource.objects.filter(database_id=database_id, resource_type=ResourceType.STATE).values())
    return HttpResponse(
        json.dumps(states),
        content_type="application/json"
    )


def collect_state(request, database_id, friendly_name):

    from database_manager.models import Database

    # Fetch database and init environment
    database = Database.objects.get(database_id = database_id)
    env = init_environment(database)
    print (database)

    # Init a new resource
    resource_id = initialise_resource(database_id, ResourceType.STATE, friendly_name)
    print ("New resource", resource_id)

    # Send request to remote executor
    callback_url = f"{settings.CONTROL_PLANE_CALLBACK_BASE_URL}/database_manager/state/collect_state_callback/"
    env.collect_state(resource_id, callback_url)

    return HttpResponse("OK")
    

@csrf_exempt
@require_http_methods(["POST"])
def collect_state_callback(request):

    data = json.loads(request.FILES["data"].read().decode("utf-8"))
    resource_id = data["resource_id"]
    print("Received collected state data. Resource id: %s" % (resource_id))

    # Save
    captured_tar = request.FILES["state"].read()
    filename = request.FILES["state"].name
    save_resource(resource_id, captured_tar, filename)

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

