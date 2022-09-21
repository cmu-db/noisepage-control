import json 

from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from resource_manager.views import initialise_resource, save_resource
from resource_manager.resource_type import ResourceType

from environments.environment import init_environment

@csrf_exempt
@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        return collect_state(request)
    return HttpResponse("Hello, world. This is state manager")


def collect_state(request):

    from database_manager.models import Database

    # Fetch database and init environment
    database_id = request.POST["database_id"]
    database = Database.objects.get(database_id = database_id)
    env = init_environment(database)
    print (database)

    # Init a new resource
    resource_id = initialise_resource(database_id, ResourceType.STATE)
    print ("New resource", resource_id)

    # TODO: Pick this from settings
    # Send request to remote executor
    callback_url = "http://ec2-34-207-82-72.compute-1.amazonaws.com:8000/database_manager/state/collect_state_callback/"
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
