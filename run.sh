#!/bin/bash

SERVER_MODE=$1

if [[ -z ${SERVER_MODE} ]]
then
    echo "Missing server mode. Command: pipenv run ./run.sh CONTROL_PLANE|PRIMARY_WORKER|EXPLORATORY_WORKER"
    exit
fi

# Presently we run the servers on fixed ports (8000, 8001, 8002).
# TODO: This needs to be fixed. Control plane discovery by worker nodes in an open problem

case ${SERVER_MODE} in
    "CONTROL_PLANE" )
        echo "Starting Control Plane"
        env $(cat config/control_plane.env | xargs) python noisepagecontrol/manage.py runserver --noreload 127.0.0.1:8000 ;;
    "PRIMARY_WORKER" )
        echo "Starting Primary Worker"
        env $(cat config/primary_worker.env | xargs) python noisepagecontrol/manage.py runserver --noreload 127.0.0.1:8001 ;;
    "EXPLORATORY_WORKER" )
        echo "Starting Exploratory Worker"
        env $(cat config/exploratory_worker.env | xargs) python noisepagecontrol/manage.py runserver --noreload 127.0.0.1:8002 ;;
    "MAKE_MIGRATIONS" )
        echo "Running makemigrations for control plane"
        env $(cat config/control_plane.env | xargs) python noisepagecontrol/manage.py makemigrations ;;
    "MIGRATE" )
        echo "Running migrate for control plane"
        env $(cat config/control_plane.env | xargs) python noisepagecontrol/manage.py migrate ;;
#########################################################################################################################################
    "FORMAT" )
        echo "Running Black"
        black .
esac