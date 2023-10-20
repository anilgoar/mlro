# Generated by Django 3.2.13 on 2022-10-07 00:34

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20221006_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploaddata',
            name='picture1',
            field=models.ImageField(upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AlterField(
            model_name='uploaddata',
            name='picture2',
            field=models.ImageField(upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AlterField(
            model_name='uploaddata',
            name='picture3',
            field=models.ImageField(upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AlterField(
            model_name='uploaddata',
            name='picture4',
            field=models.ImageField(upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AlterField(
            model_name='uploaddata',
            name='rel_pic1',
            field=models.ImageField(null=True, upload_to=apps.home.models.UploadData.path_and_rename),
        ),
        migrations.AlterField(
            model_name='uploaddata',
            name='rel_pic2',
            field=models.ImageField(null=True, upload_to=apps.home.models.UploadData.path_and_rename),
        ),
    ]