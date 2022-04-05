import json
import subprocess
import pathlib
import os
from threading import Thread
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

DIR_PATH = pathlib.Path(__file__).resolve().parent
START_EXPLORATORY_SCRIPT = os.path.join(DIR_PATH, 'scripts/start_exploratory_cluster.sh')
STOP_EXPLORATORY_SCRIPT = os.path.join(DIR_PATH, 'scripts/stop_exploratory_cluster.sh')


def index(request):
    return HttpResponse("Hello, world. This is the exploratory_worker")


@csrf_exempt
@require_http_methods(["POST"])
def launch_exploratory_cluster(request):
    snapshot = json.loads(request.body)['snapshot']
    # asynchronously spins up a pg instance
    thread = Thread(target=start_exploratory_cluster, args=(snapshot,))
    thread.start()

    return HttpResponse()


def start_exploratory_cluster(snapshot):
    # TODO Tim: probe an available port from 10000 instead of hard-coding
    exploratory_cluster_port = 10000
    print(f"starting exploratory Postgres cluster on port {exploratory_cluster_port}...")

    args = ['sudo', '-u', 'postgres', START_EXPLORATORY_SCRIPT, str(exploratory_cluster_port)]
    if snapshot:
        print("taking snapshot from replica cluster...")
        args.append('-s')
    try:
        res = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res.wait()
    except OSError:
        print(f"Error while executing {START_EXPLORATORY_SCRIPT}")
        return
    if res.returncode != 0:
        print(f"{START_EXPLORATORY_SCRIPT} returncode != 0")
        print(res.stdout.read())
        print(res.stderr.read())
        return
    print("done!")

    # TODO Tim: send back the port to control plane
    print(f"TODO: send exploratory_cluster_port: {exploratory_cluster_port} back to control plane!!!")


def collect_training_data(request):
    pass

@csrf_exempt
@require_http_methods(["DELETE"])
def stop_exploratory_cluster(request):
    body = json.loads(request.body)
    port = body['port']
    
    print(f"Stopping exploratory Postgres cluster on port {port}...")
    args = ['sudo', '-u', 'postgres', STOP_EXPLORATORY_SCRIPT, str(port)]
    res = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res.wait()

    return HttpResponse()
