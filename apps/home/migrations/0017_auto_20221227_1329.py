# Generated by Django 2.2.12 on 2022-12-27 13:29

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20221220_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploaddata',
            name='altaction1',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altaction2',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altaremarks1',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altaremarks2',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altmlro_remarks1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altmlro_remarks2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altpicture1',
            field=models.ImageField(null=True, upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altpicture2',
            field=models.ImageField(null=True, upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altpicture_sc1',
            field=models.CharField(max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altpicture_sc2',
            field=models.CharField(max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altscreen1',
            field=models.ImageField(null=True, upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='altscreen2',
            field=models.ImageField(null=True, upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='matchcase',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='rating',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='uploaddata',
            name='remarks',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
