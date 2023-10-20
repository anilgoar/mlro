import os
import time
from uuid import uuid4

from django.db import models

class UploadData(models.Model):
    def _get_upload_to(instance, filename):
        return 'images/%f.jpg' % time.time(),filename

    def path_and_rename(instance, filename):
        upload_to = 'photos'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    id = models.AutoField(primary_key=True)
    profile_id = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=30)
    remarks = models.CharField(max_length=2000,null=True)
    name_of_identity = models.CharField(max_length=100)
    picture1 = models.ImageField(upload_to=path_and_rename)
    picture2 = models.ImageField(upload_to=path_and_rename)
    picture3 = models.ImageField(upload_to=path_and_rename)
    picture4 = models.ImageField(upload_to=path_and_rename)
    picture_sc1 = models.CharField(max_length=600)
    picture_sc2 = models.CharField(max_length=600)
    picture_sc3 = models.CharField(max_length=600)
    picture_sc4 = models.CharField(max_length=600)
    Relation1 = models.CharField(max_length=30,null=True)
    rel_pic1 = models.ImageField(upload_to=path_and_rename,null=True)
    rel_web1 = models.CharField(max_length=600,null=True)
    rel_profile1 = models.CharField(max_length=30, null=True)
    Relation2 = models.CharField(max_length=30,null=True)
    rel_pic2 = models.ImageField(upload_to=path_and_rename,null=True)
    rel_web2 = models.CharField(max_length=600,null=True)
    rel_profile2 = models.CharField(max_length=30,null=True)
    aremarks = models.CharField(max_length=400,null=True)
    aremarks1 = models.CharField(max_length=400, null=True)
    aremarks2 = models.CharField(max_length=400, null=True)
    created = models.DateTimeField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    user = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=10, null=True, default='0')
    action = models.CharField(max_length=40, null=True)
    action1 = models.CharField(max_length=40, null=True)
    action2 = models.CharField(max_length=40, null=True)
    mlro_remarks = models.CharField(max_length=400, null=True)
    mlro_remarks1 = models.CharField(max_length=400, null=True)
    mlro_remarks2 = models.CharField(max_length=400, null=True)
    action_start_date = models.DateTimeField(null=True)
    action_date = models.DateTimeField(null=True)
    action_status = models.CharField(max_length=10, null=True, default='0')
    task_time = models.DateTimeField(null=True)
    mlro_id = models.CharField(max_length=255, null=True)
    altpicture1 = models.ImageField(upload_to=path_and_rename,null=True)
    altscreen1 = models.ImageField(upload_to=path_and_rename,null=True)
    altpicture2 = models.ImageField(upload_to=path_and_rename,null=True)
    altscreen2 = models.ImageField(upload_to=path_and_rename,null=True)
    altpicture_sc1 = models.CharField(max_length=600,null=True)
    altaremarks1 = models.CharField(max_length=400, null=True)
    altpicture_sc2 = models.CharField(max_length=600,null=True)
    altaremarks2 = models.CharField(max_length=400, null=True)
    matchcase = models.CharField(max_length=100, null=True)
    rating = models.CharField(max_length=10, null=True)
    altaction1 = models.CharField(max_length=40, null=True)
    altmlro_remarks1 = models.CharField(max_length=255, null=True)
    altaction2 = models.CharField(max_length=40, null=True)
    altmlro_remarks2 = models.CharField(max_length=255, null=True)
    hold_case = models.CharField(max_length=10, null=True)	



    def __str__(self):
        return self.name

    class Meta:
        db_table = 'upload_data'

class UserLogs(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    event = models.CharField(max_length=30)
    event_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user_logs'

class AnalystLogs(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    task_id = models.CharField(max_length=30,null=True)
    task_start = models.DateTimeField(null=True)
    task_end = models.DateTimeField(null=True)
    break_start = models.DateTimeField(null=True)
    break_end = models.DateTimeField(null=True)
    break_code = models.CharField(max_length=50,null=True)
    break_chk = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'analyst_logs'


class UploadUniqueData(models.Model):
    def _get_upload_to(instance, filename):
        return 'images/%f.jpg' % time.time(),filename

    def path_and_rename(instance, filename):
        upload_to = 'photos'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    id = models.AutoField(primary_key=True)
    upload_id = models.CharField(max_length=30)
    profile_id = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=30)
    remarks = models.CharField(max_length=300)
    relation = models.CharField(max_length=50)
    picture = models.ImageField(upload_to=path_and_rename)
    sc_picture = models.ImageField(upload_to=path_and_rename)
    web_link = models.CharField(max_length=600)
    remarks = models.CharField(max_length=600)
    mlro_remarks = models.CharField(max_length=600)
    created = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'upload_unique_data'
