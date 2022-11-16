import json 
import datetime
import tarfile
import os 

from django.http import HttpResponse, FileResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from resource_manager.views import initialise_resource, save_resource, get_resource_filepath, does_resource_exist
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
        return collect_workload(request, database_id, data["num_chunks"])
    elif request.method == "GET":
        return get_workloads(request, database_id)


def collect_workload(request, database_id, num_chunks):

    from database_manager.models import Database

    # Fetch database and init environment
    database = Database.objects.get(database_id = database_id)
    env = init_environment(database)

    callback_url = f"{settings.CONTROL_PLANE_CALLBACK_BASE_URL}/database_manager/workload/collect_workload_callback/"
    env.collect_workload(num_chunks, callback_url)

    # Send request to remote executor
    return HttpResponse("OK")


@csrf_exempt
@require_http_methods(["POST"])
def collect_workload_callback(request):

    data = json.loads(request.FILES["data"].read().decode("utf-8"))

    database_id = data["database_id"]
    # Hack, we should only request for num_chunks = 1 in collect workload
    # Needs to be redesigned in the future, don't have the time now


    temp_file_name = str(uuid.uuid4())
    with open(temp_file_name, 'wb') as fp:
        fp.write(request.FILES["workload"].read())
    tar = tarfile.open(temp_file_name)

    for chunk in data["meta_data"]:
        file_name = chunk["file_name"]
        collected_at = datetime.datetime.strptime(file_name, "postgresql-%Y-%m-%d_%H%M%S.csv")
        friendly_name = "%s_%s" % (database_id, file_name)

        print("Received collected data. friendly_name: %s" % (friendly_name))

        # If resource exists do not save it again
        if does_resource_exist(friendly_name):
            return HttpResponse("OK")
    
        print ("Creating new resource")
        resource_id = initialise_resource(database_id, ResourceType.WORKLOAD, friendly_name, meta_data = chunk)
        resource = save_resource(resource_id, tar.extractfile(file_name).read(), friendly_name, collected_at)
        print ("created", get_resource_filepath(resource))

    tar.close()
    os.remove(temp_file_name)
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
