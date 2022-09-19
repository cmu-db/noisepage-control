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
        return collect_workload(request)
    return HttpResponse("Hello, world. This is workload manager")


def collect_workload(request):

    from database_manager.models import Database


    # Fetch database and init environment
    database_id = request.POST["database_id"]
    time_period = request.POST["time_period"]

    database = Database.objects.get(database_id = database_id)
    env = init_environment(database)
    print (database)



    # Init a new resource
    resource_id = initialise_resource(database_id, ResourceType.WORKLOAD)
    print ("New resource", resource_id)

    env.collect_workload(time_period, resource_id)

    # Send request to remote executor
    return HttpResponse("OK")
    
