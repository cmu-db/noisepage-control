import sys
from django.apps import AppConfig
from threading import Thread

from database_manager.services.command_queue.consumer import init_command_consumer
from database_manager.services.workload_manager.views import pull_workload_for_all_databases
from database_manager.services.state_manager.views import collect_state_for_all_databases

class DatabaseManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database_manager'


    def ready(self):
        """
        Init command consumer

        TODO: Add robustness to the consumer thread.
        What happens if it fails?
        """
        # Do not start the consumer thread or the cron jobs when running "manage.py migrate" etc.
        is_manage_py = any(arg.casefold().endswith("manage.py") for arg in sys.argv)
        is_runserver = any(arg.casefold() == "runserver" for arg in sys.argv)
        if is_manage_py and not is_runserver:
            return

        thread = Thread(target=init_command_consumer)
        thread.start()

        # For scheduling workload pulls
        from apscheduler.schedulers.background import BackgroundScheduler
        import logging
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

        scheduler = BackgroundScheduler()

        # Workloads are chunked at 5 minutes on primary db;
        scheduler.add_job(pull_workload_for_all_databases, trigger='cron', minute = "*/5")

        # Collect state every 5 minutes
        scheduler.add_job(collect_state_for_all_databases, trigger='cron', minute = "4/5")

        scheduler.start()