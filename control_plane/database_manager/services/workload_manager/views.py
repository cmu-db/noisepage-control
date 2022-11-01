import json 

from django.http import HttpResponse, FileResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from resource_manager.views import initialise_resource, save_resource, get_resource_filepath
from resource_manager.resource_type import ResourceType

from environments.environment import init_environment


@csrf_exempt
@require_http_methods(["GET"])
def index(request):
    return HttpResponse("Hello, world. This is workload manager")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def workloads(request, database_id):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        return collect_workload(request, database_id, data["time_period"], data["friendly_name"])
    elif request.method == "GET":
        return get_workloads(request, database_id)


def collect_workload(request, database_id, time_period, friendly_name):

    from database_manager.models import Database

    # Fetch database and init environment
    database = Database.objects.get(database_id = database_id)
    env = init_environment(database)

    # Init a new resource
    resource_id = initialise_resource(
        database_id, 
        ResourceType.WORKLOAD, 
        friendly_name, 
        {"time_period": time_period}
    )
    print ("New resource", resource_id)

    callback_url = f"{settings.CONTROL_PLANE_CALLBACK_BASE_URL}/database_manager/workload/collect_workload_callback/"
    env.collect_workload(time_period, resource_id, callback_url)

    # Send request to remote executor
    return HttpResponse("OK")


@csrf_exempt
@require_http_methods(["POST"])
def collect_workload_callback(request):

    data = json.loads(request.FILES["data"].read().decode("utf-8"))

    resource_id = data["resource_id"]
    
    print("Received collected data. Resource id: %s" % (resource_id))

    captured_workload_tar = request.FILES["workload"].read()
    captured_workload_filename = request.FILES["workload"].name

    save_resource(resource_id, captured_workload_tar, captured_workload_filename)

    return HttpResponse("OK")


@csrf_exempt
@require_http_methods(["GET"])
def get_workloads(request, database_id):
    # get workload with datbase_id
    from resource_manager.models import Resource
    workloads = list(Resource.objects.filter(database_id=database_id, resource_type=ResourceType.WORKLOAD).values())
    return HttpResponse(
        json.dumps(workloads, default=str),
        content_type="application/json"
    )

@csrf_exempt
@require_http_methods(["GET"])
def download_workload(request, workload_id):

    from resource_manager.models import Resource
    workload = Resource.objects.get(resource_id = workload_id)

    if workload.available == False:
        return HttpResponse("File not available")

    filepath = get_resource_filepath(workload)
    print (filepath)
    
    fp = open(filepath, "rb")
    response = FileResponse(fp)

    response['Content-Type'] = "application/gzip"
    return response
