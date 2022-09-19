from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def index(request):
    return HttpResponse("Hello, world. This is the control_plane")