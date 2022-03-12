from django.http import HttpResponse
from control_plane.message_queue.producer import publish_message

# Create your views here.
def index(request):

    publish_message()
    return HttpResponse("Hello, world. This is the control_plane")
