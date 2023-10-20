# Generated by Django 3.2.13 on 2022-10-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20221006_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploaddata',
            name='Relation1',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='Relation2',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='aremarks',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='rel_pic1',
            field=models.ImageField(null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='rel_pic2',
            field=models.ImageField(null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='rel_profile2',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='rel_web1',
            field=models.CharField(max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='rel_web2',
            field=models.CharField(max_length=600, null=True),
        ),
    ]