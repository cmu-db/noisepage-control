# Generated by Django 4.0.3 on 2022-03-30 00:05

import control_plane.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TuningEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=120)),
                ('event_type', models.CharField(max_length=120)),
                ('parent_event_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=120), blank=True, size=None)),
                ('tuning_id', models.CharField(max_length=36)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TuningInstance',
            fields=[
                ('primary_url', models.CharField(max_length=30)),
                ('primary_port', models.CharField(max_length=5)),
                ('replica_url', models.CharField(max_length=30)),
                ('replica_port', models.CharField(max_length=5)),
                ('state', models.JSONField(default=control_plane.models.tuningInstance_state_default, verbose_name='state')),
                ('tuning_id', models.CharField(default=control_plane.models.autogenerate_uuid, max_length=36, primary_key=True, serialize=False)),
            ],
        ),
    ]
