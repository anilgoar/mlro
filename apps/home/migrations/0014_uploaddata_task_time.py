# Generated by Django 3.2.13 on 2022-10-09 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_uploaddata_action_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploaddata',
            name='task_time',
            field=models.DateTimeField(null=True),
        ),
    ]