# Generated by Django 3.2.13 on 2022-10-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploaddata',
            name='status',
            field=models.CharField(default='0', max_length=10, null=True),
        ),
    ]
