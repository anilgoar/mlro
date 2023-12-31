# Generated by Django 2.2.12 on 2022-10-27 06:06

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_uploaddata_task_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadUniqueData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('upload_id', models.CharField(max_length=30)),
                ('profile_id', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('dob', models.CharField(max_length=30)),
                ('relation', models.CharField(max_length=50)),
                ('picture', models.ImageField(upload_to=apps.home.models.UploadUniqueData.path_and_rename)),
                ('sc_picture', models.ImageField(upload_to=apps.home.models.UploadUniqueData.path_and_rename)),
                ('web_link', models.CharField(max_length=600)),
                ('remarks', models.CharField(max_length=600)),
                ('mlro_remarks', models.CharField(max_length=600)),
                ('created', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'upload_unique_data',
            },
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='action1',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='action2',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='aremarks1',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='aremarks2',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='mlro_remarks1',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='mlro_remarks2',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
