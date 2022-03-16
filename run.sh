#!/bin/bash

SERVER_MODE=$1

if [[ -z ${SERVER_MODE} ]]
then
    echo "Missing server mode. Command: pipenv run run.sh CONTROL_PLANE|PRIMARY_WORKER|EXPLORATORY_WORKER"
    exit
fi

case ${SERVER_MODE} in
    "CONTROL_PLANE" )
        echo "Starting Control Plane"
        env $(cat config/control_plane.env | xargs) python noisepagecontrol/manage.py runserver ;;
    "PRIMARY_WORKER" )
        echo "Starting Primary Worker"
        env $(cat config/primary_worker.env | xargs) python noisepagecontrol/manage.py runserver ;;
    "EXPLORATORY_WORKER" )
        echo "Starting Exploratory Worker"
        env $(cat config/exploratory_worker.env | xargs) python noisepagecontrol/manage.py runserver ;;
esac

env $(cat config/control_plane.env | xargs) python noisepagecontrol/manage.py runserver



# env $(cat config/control_plane.env | xargs) python noisepagecontrol/manage.py makemigrations
# env $(cat config/control_plane.env | xargs) python noisepagecontrol/manage.py migrate