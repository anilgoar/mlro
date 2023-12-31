# Generated by Django 2.2.12 on 2023-01-27 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20230124_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalystLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=30)),
                ('task_id', models.CharField(max_length=30, null=True)),
                ('task_start', models.DateTimeField(null=True)),
                ('task_end', models.DateTimeField(null=True)),
                ('break_start', models.DateTimeField(null=True)),
                ('break_end', models.DateTimeField(null=True)),
                ('break_code', models.CharField(max_length=50, null=True)),
                ('break_chk', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'analyst_logs',
            },
        ),
    ]
