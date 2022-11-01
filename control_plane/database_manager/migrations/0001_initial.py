# Generated by Django 4.1.2 on 2022-11-01 01:24

import database_manager.database_state_types
import database_manager.models
import database_manager.services.command_queue.models
import database_manager.types.action_status
import database_manager.types.tuningstatus
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import environments.environment_types


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resource_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('command_id', models.CharField(default=database_manager.services.command_queue.models.autogenerate_uuid, max_length=36, primary_key=True, serialize=False)),
                ('database_id', models.CharField(max_length=36)),
                ('parent_command_ids', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=36), blank=True, size=None)),
                ('command_type', models.CharField(max_length=120)),
                ('completed', models.BooleanField(default=False)),
                ('config', models.JSONField(default=dict, verbose_name='config')),
            ],
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('database_id', models.CharField(default=database_manager.models.autogenerate_uuid, max_length=36, primary_key=True, serialize=False)),
                ('environment_type', models.CharField(choices=[(environments.environment_types.EnvironmentType['SELF_MANAGED_POSTGRES'], 'Self managed postgres'), (environments.environment_types.EnvironmentType['AWS_RDS_POSTGRES'], 'AWS RDS Postgres')], max_length=120)),
                ('active', models.BooleanField(default=True)),
                ('state', models.CharField(choices=[(database_manager.database_state_types.DatabaseStateType['REGISTERING'], 'REGISTERING'), (database_manager.database_state_types.DatabaseStateType['HEALTHY'], 'HEALTHY'), (database_manager.database_state_types.DatabaseStateType['UNHEALTHY'], 'UNHEALTHY'), (database_manager.database_state_types.DatabaseStateType['TUNING'], 'TUNING'), (database_manager.database_state_types.DatabaseStateType['COLLECTING_WORKLOAD'], 'COLLECTING_WORKLOAD'), (database_manager.database_state_types.DatabaseStateType['COLLECTING_METRICS'], 'COLLECTING_METRICS'), (database_manager.database_state_types.DatabaseStateType['COLLECTING_STATE'], 'COLLECTING_STATE')], max_length=120)),
                ('errors', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TuningAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tuning_action_id', models.CharField(default=database_manager.models.autogenerate_uuid, max_length=36)),
                ('database_id', models.CharField(max_length=36)),
                ('tuning_instance_id', models.CharField(max_length=36)),
                ('command', models.CharField(max_length=512)),
                ('benefit', models.FloatField()),
                ('reboot_required', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[(database_manager.types.action_status.ActionStatusType['NOT_APPLIED'], 'NOT_APPLIED'), (database_manager.types.action_status.ActionStatusType['APPLYING'], 'APPLYING'), (database_manager.types.action_status.ActionStatusType['APPLIED'], 'APPLIED'), (database_manager.types.action_status.ActionStatusType['FAILED'], 'FAILED')], max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TuningInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tuning_instance_id', models.CharField(default=database_manager.models.autogenerate_uuid, max_length=36)),
                ('database_id', models.CharField(max_length=36)),
                ('friendly_name', models.CharField(max_length=36, unique=True)),
                ('workload_id', models.CharField(max_length=36)),
                ('state_id', models.CharField(max_length=36)),
                ('status', models.CharField(choices=[(database_manager.types.tuningstatus.TuningStatusType['RUNNING'], 'RUNNING'), (database_manager.types.tuningstatus.TuningStatusType['FINISHED'], 'FINISHED'), (database_manager.types.tuningstatus.TuningStatusType['FAILED'], 'FAILED')], max_length=32)),
                ('finished_at', models.DateField(blank=True)),
                ('action_name', models.CharField(blank=True, max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='SelfManagedPostgresConfig',
            fields=[
                ('database', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='database_manager.database')),
                ('db_name', models.CharField(max_length=120)),
                ('primary_host', models.CharField(max_length=120)),
                ('primary_ssh_port', models.CharField(max_length=120)),
                ('primary_ssh_user', models.CharField(max_length=120)),
                ('primary_pg_user', models.CharField(max_length=120)),
                ('primary_pg_port', models.CharField(max_length=120)),
                ('replica_host', models.CharField(max_length=120)),
                ('replica_ssh_port', models.CharField(max_length=120)),
                ('replica_ssh_user', models.CharField(max_length=120)),
                ('replica_pg_user', models.CharField(max_length=120)),
                ('replica_pg_port', models.CharField(max_length=120)),
                ('primary_ssh_key', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='primary_ssh_key', to='resource_manager.resource')),
                ('replica_ssh_key', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='replica_ssh_key', to='resource_manager.resource')),
            ],
        ),
    ]
