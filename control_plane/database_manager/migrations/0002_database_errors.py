# Generated by Django 4.1.1 on 2022-09-09 14:43

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='errors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, size=None),
        ),
    ]
