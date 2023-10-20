# Generated by Django 2.2.12 on 2023-01-24 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20221227_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=30)),
                ('event', models.CharField(max_length=30)),
                ('event_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'user_logs',
            },
        ),
        migrations.AddField(
            model_name='uploaddata',
            name='hold_case',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
