# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import csv
import xlwt
import logging

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.db.models import DurationField, ExpressionWrapper, F, Sum, Avg
from django.db.models.functions import Cast
from django.http import HttpResponse, HttpResponseRedirect, response
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import pandas as pd
from django.contrib import messages

from apps.home.forms import UploadsForm
from apps.home.models import UploadData, UploadUniqueData, AnalystLogs, UserLogs
from django.core.files.images import get_image_dimensions


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

def decode_utf8(line_iterator):
    for line in line_iterator:
        yield line.decode('utf-8')

@login_required(login_url="/login/")
def upload_data(request):
    data = {}
    if "GET" == request.method:
        return render(request, "home/upload_data.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        # print(list(request.FILES))

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_data"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("upload_data"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # next(lines, None)
        # loop over the lines and save them in db. If error , store as string and then display
        # print(len(lines))
        flag_header = True

        for line in lines:
            if flag_header:
                flag_header = False
                continue
            fields = line.split(",")
            data_dict = {}

            try:
                data_dict["profile_id"] = fields[0]
                data_dict["name"] = fields[1]
                data_dict["dob"] = fields[2]
                data_dict["remarks"] = fields[3]
                data_dict["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # print(data_dict)
                form = UploadsForm(data_dict)
                if form.is_valid():
                    form.save()
                    messages.error(request, 'File Imported Successfuly')
                else:
                    messages.error("error_logger").error(form.errors.as_json())
            except Exception as e:
                break
                pass

    except Exception as e:
        print(e)

        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload_data"))


@login_required(login_url="/login/")
def feedback(request):
    user = request.user
    idx = request.GET.get('idx')
    viewdata = None
    url_name = None
    try:
        user = User.objects.get(username=user)
        if idx is None or idx=="":
            viewdata = UploadData.objects.filter(status='0',user=user.username).first()
        else:
            viewdata = UploadData.objects.filter(user__isnull=True, id=idx).first()
            id = viewdata.id
            upuser = viewdata.user
            exdata = UploadData.objects.get(id=id)
            exdata.start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exdata.user = user.username

            exdata.save()
            exdata1 = AnalystLogs()
            exdata1.user_id = user.username
            exdata1.task_id = id
            exdata1.task_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exdata1.save()

        if viewdata is None:
            viewdata = UploadData.objects.filter(user__isnull=True, status='0').first()
            url_name = str(viewdata.name).split(" ")[0]
            id = viewdata.id
            upuser = viewdata.user
            exdata = UploadData.objects.get(id=id)
            exdata.start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exdata.user = user.username

            exdata.save()

            exdata1 = AnalystLogs()
            exdata1.user_id = user.username
            exdata1.task_id = id
            exdata1.task_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exdata1.save()
        else:
            url_name = str(viewdata.name).split(" ")[0]
        if viewdata is None:
            #print("no")
            return render(request, "home/feedback.html",{"viewdata":viewdata,"url_name":url_name})

    except Exception as e:
        print(e)
    #print(6)
    return render(request, "home/feedback.html",{"viewdata": viewdata,"url_name":url_name})

@login_required(login_url="/login/")
def feedback_update(request):
    #print(request.POST)

    if request.method == 'POST':

        picture1 = request.FILES.get('picture1')
        picture_sc1 = request.POST['picture_sc1']
        picture2 = request.FILES.get('picture2')
        aremarks = request.POST['aremarks']

        matchcase = request.POST.getlist('matchcase[]')
        rating = request.POST.get('rating')

        altpicture1 = request.FILES.get('altpicture1')
        altpicture_sc1 = request.POST['altpicture_sc1']
        altscreen1 = request.FILES.get('altscreen1')
        altaremarks1 = request.POST['altaremarks1']

        altpicture2 = request.FILES.get('altpicture2')
        altpicture_sc2 = request.POST['altpicture_sc2']
        altscreen2 = request.FILES.get('altscreen2')
        altaremarks2 = request.POST['altaremarks2']

        Relation1 = request.POST['Relation1']
        rel_pic1 = request.FILES.get('rel_pic1')
        rel_web1 = request.POST['rel_web1']
        rel_profile1 = request.POST['rel_profile1']
        picture3 = request.FILES.get('picture3')
        aremarks1 = request.POST['aremarks1']


        Relation2 = request.POST['Relation2']
        rel_pic2 = request.FILES.get('rel_pic2')
        rel_web2 = request.POST['rel_web2']
        rel_profile2 = request.POST['rel_profile2']
        picture4 = request.FILES.get('picture4')
        aremarks2 = request.POST['aremarks2']
        hold_case = request.POST.get('hold_case')
        btn_val = request.POST.get('Save')

        if picture1 is not None:
            width, height = get_image_dimensions(picture1)
            if width < 256 or height < 256:
                messages.error(request, "Image dimensions is too small, minimum is 256x256")
                return HttpResponseRedirect(reverse("feedback"))
            if width > 8192 or height > 8192:
                messages.error(request, "Image dimensions is too Big, maximum is 8192x8192")
                return HttpResponseRedirect(reverse("feedback"))
            if picture_sc1 is None or picture2 is None:
                messages.error(request, "Any field is missing")
                return HttpResponseRedirect(reverse("feedback"))
            if picture1.name.endswith('.jfif'):
                messages.error(request, 'Only Allowed PNG,JPG,JPEG')
                return HttpResponseRedirect(reverse("feedback"))    

        #newtim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")-datetime.datetime.request.POST['starttime']
        #print(newtim.days)
        #quit()
        id = request.POST['id']
        #form = UploadsForm(request.POST or None, request.FILES or None, instance=id)
        exdata = UploadData.objects.get(id=id)
        exdata1 = UploadUniqueData()
   # if form.is_valid():
        exdata.picture1 = picture1
        exdata.picture_sc1 = picture_sc1
        exdata.picture2 = picture2
        exdata.aremarks = aremarks

        exdata.matchcase = matchcase
        exdata.rating = rating

        exdata.altpicture1 = altpicture1
        exdata.altpicture_sc1 = altpicture_sc1
        exdata.altscreen1 = altscreen1
        exdata.altaremarks1 = altaremarks1

        exdata.altpicture2 = altpicture2
        exdata.altpicture_sc2 = altpicture_sc2
        exdata.altscreen2 = altscreen2
        exdata.altaremarks2 = altaremarks2

        exdata.Relation1 = Relation1
        exdata.rel_pic1 = rel_pic1
        exdata.rel_web1 = rel_web1
        exdata.rel_profile1 = rel_profile1
        exdata.picture3 = picture3
        exdata.aremarks1 = aremarks1

        exdata.Relation2 = Relation2
        exdata.rel_pic2 = rel_pic2
        exdata.rel_web2 = rel_web2
        exdata.rel_profile2 = rel_profile2
        exdata.picture4 = picture4
        exdata.aremarks2 = aremarks2
        exdata.hold_case = hold_case

        #exdata.task_time = newtim.days

        exdata.status = '1'
        exdata.end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exdata.save()
        exdata1.save()

        exdata2 = AnalystLogs.objects.get(task_id=id)
        exdata2.task_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exdata2.save()

        #img_object = exdata.instance

    if btn_val == 'Save':
        return HttpResponseRedirect(reverse('feedback'))
    else:
        return HttpResponseRedirect(reverse('break_add'))

@login_required(login_url="/login/")
def details(request):
    objs = UploadData.objects.filter(status='1').exclude(picture1='')
    return render(request, "home/details.html",{'objs':objs})

@login_required(login_url="/login/")
def details_view(request):
    detailidv = request.GET['abc']
    objs = UploadData.objects.filter(id=detailidv).first()
    #print(objs)
    if objs.action_start_date is None:
        id = objs.id
        exdata = UploadData.objects.get(id=id)
        exdata.action_start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        exdata.save()
    return render(request, "home/details_view.html",{'objs':objs})

@login_required(login_url="/login/")
def details_view_update(request):
    user = request.user
    if request.method == 'POST':
        action = request.POST['action']
        mlro_remarks = request.POST['mlro_remarks']

        altaction1 = request.POST['altaction1']
        altmlro_remarks1 = request.POST['altmlro_remarks1']

        altaction2 = request.POST['altaction2']
        altmlro_remarks2 = request.POST['altmlro_remarks2']

        action1 = request.POST['action1']
        mlro_remarks1 = request.POST['mlro_remarks1']
        action2 = request.POST['action2']
        mlro_remarks2 = request.POST['mlro_remarks2']

        id = request.POST['id']
        #form = UploadsForm(request.POST or None, request.FILES or None, instance=id)
        exdata = UploadData.objects.get(id=id)
   # if form.is_valid():

        exdata.action = action
        exdata.mlro_remarks = mlro_remarks

        exdata.altaction1 = altaction1
        exdata.altmlro_remarks1 = altmlro_remarks1

        exdata.altaction2 = altaction2
        exdata.altmlro_remarks2 = altmlro_remarks2

        exdata.action1 = action1
        exdata.mlro_remarks1 = mlro_remarks1
        exdata.action2 = action2
        exdata.mlro_remarks2 = mlro_remarks2

        exdata.action_status = '1'
        exdata.action_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exdata.mlro_id = user.username
        exdata.save()

        #img_object = exdata.instance

    return HttpResponseRedirect(reverse('details'))


@login_required(login_url="/login/")
def rej_details(request):
    user = request.user
    user = User.objects.get(username=user)
    objs = UploadData.objects.filter(user=user.username) & UploadData.objects.filter(action='Reject') | UploadData.objects.filter(action1='Reject') | UploadData.objects.filter(action2='Reject')
    return render(request, "home/rej_details.html",{'objs':objs})

@login_required(login_url="/login/")
def rej_details_view(request,str):
    user = request.user
    objs = UploadData.objects.filter(id=str).first()
    #print(user)
    exdata1 = AnalystLogs()
    exdata1.user_id = user.username
    exdata1.task_id = str
    exdata1.task_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    exdata1.save()
    if objs.action_start_date is None:
        id = objs.id
        exdata = UploadData.objects.get(id=id)
        exdata.action_start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        exdata.save()

        exdata1 = AnalystLogs()
        exdata1.user_id = user.username
        exdata1.task_id = id
        exdata1.task_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exdata1.save()
    return render(request, "home/rej_details_view.html",{'objs':objs})


@login_required(login_url="/login/")
def rej_details_view_update(request):
    if request.method == 'POST':

        action = request.POST.get('action')
        action1 = request.POST.get('action1')
        action2 = request.POST.get('action2')
        id = request.POST['id']
        #print(id)
        if action == 'Reject':
            picture1 = request.FILES.get('picture1')
            picture_sc1 = request.POST['picture_sc1']
            picture2 = request.FILES.get('picture2')
            aremarks = request.POST['aremarks']

            matchcase = request.POST.getlist('matchcase[]')
            rating = request.POST.get('rating')

            altpicture1 = request.FILES.get('altpicture1')
            altpicture_sc1 = request.POST['altpicture_sc1']
            altscreen1 = request.FILES.get('altscreen1')
            altaremarks1 = request.POST['altaremarks1']

            altpicture2 = request.FILES.get('altpicture2')
            altpicture_sc2 = request.POST['altpicture_sc2']
            altscreen2 = request.FILES.get('altscreen2')
            altaremarks2 = request.POST['altaremarks2']



        if action1 == 'Reject':
            Relation1 = request.POST['Relation1']
            rel_pic1 = request.FILES.get('rel_pic1')
            rel_web1 = request.POST['rel_web1']
            rel_profile1 = request.POST['rel_profile1']
            picture3 = request.FILES.get('picture3')
            aremarks1 = request.POST['aremarks1']

        if action2 == 'Reject':
            Relation2 = request.POST['Relation2']
            rel_pic2 = request.FILES.get('rel_pic2')
            rel_web2 = request.POST['rel_web2']
            rel_profile2 = request.POST['rel_profile2']
            picture4 = request.FILES.get('picture4')
            aremarks2 = request.POST['aremarks2']

        if picture1 is not None:
            width, height = get_image_dimensions(picture1)
            if width < 256 or height < 256:
                messages.error(request, "Image dimensions is too small, minimum is 256x256")
                return HttpResponseRedirect(reverse("rej_details_view",args={id}))
            if width > 8192 or height > 8192:
                messages.error(request, "Image dimensions is too Big, maximum is 8192x8192")
                return HttpResponseRedirect(reverse("rej_details_view",args={id}))
            if picture_sc1 is None or picture2 is None:
                messages.error(request, "Any field is missing")
                return HttpResponseRedirect(reverse("rej_details_view",args={id}))
            if picture1.name.endswith('.jfif'):
                messages.error(request, 'Only Allowed PNG,JPG,JPEG')
                return HttpResponseRedirect(reverse("rej_details_view",args={id}))

        #print(action2)
        # newtim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")-datetime.datetime.request.POST['starttime']
        # print(newtim.days)
        # quit()

        # form = UploadsForm(request.POST or None, request.FILES or None, instance=id)
        exdata = UploadData.objects.get(id=id)
        exdata1 = UploadUniqueData()
        # if form.is_valid():
        if action == 'Reject':
            exdata.picture1 = picture1
            exdata.picture_sc1 = picture_sc1
            exdata.picture2 = picture2
            exdata.aremarks = aremarks
            exdata.action   =""

            exdata.matchcase = matchcase
            exdata.rating = rating

            exdata.altpicture1 = altpicture1
            exdata.altpicture_sc1 = altpicture_sc1
            exdata.altscreen1 = altscreen1
            exdata.altaremarks1 = altaremarks1

            exdata.altpicture2 = altpicture2
            exdata.altpicture_sc2 = altpicture_sc2
            exdata.altscreen2 = altscreen2
            exdata.altaremarks2 = altaremarks2


        if action1 == 'Reject':
            exdata.Relation1 = Relation1
            exdata.rel_pic1 = rel_pic1
            exdata.rel_web1 = rel_web1
            exdata.rel_profile1 = rel_profile1
            exdata.picture3 = picture3
            exdata.aremarks1 = aremarks1
            exdata.action1 = ""

        if action2 == 'Reject':
            exdata.Relation2 = Relation2
            exdata.rel_pic2 = rel_pic2
            exdata.rel_web2 = rel_web2
            exdata.rel_profile2 = rel_profile2
            exdata.picture4 = picture4
            exdata.aremarks2 = aremarks2
            exdata.action2 = ""

        # exdata.task_time = newtim.days

        exdata.status = '1'
        exdata.end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exdata.save()
        exdata1.save()

        #exdata2 = AnalystLogs.objects.all().filter(task_id=id)
        #exdata2.task_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #exdata2.save()

        # img_object = exdata.instance

    return HttpResponseRedirect(reverse('rej_details'))




@login_required(login_url="/login/")
def report(request):

    return render(request, "home/report.html")

@login_required(login_url="/login/")
def report_extract(request):
    if request.method == 'POST':
        cdate = request.POST['cDate']
        #print(cdate)
        start_date = datetime.strptime(request.POST['start_date'], "%m/%d/%Y").strftime('%Y-%m-%d')+" 00:00:00"
        end_date = datetime.strptime(request.POST['end_date'], "%m/%d/%Y").strftime('%Y-%m-%d')+" 23:59:59"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export_data.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['Profile Id', 'Name','DOB','Upload Remarks', 'Task Start Time', 'Task End Time', 'MLRO Start Time', 'MLRO End Time', 'Task Time', 'MLRO Time' ,'Picture','web link','screen short','Remarks','Match Case','Source Rating','Alt Picture1','Alt web link1','Alt screen short1','Alt Remarks1','Alt Picture2','Alt web link2','Alt screen short2','Alt Remarks2','Analyst','Hold Status','approval status','MLRO Remarks','MLRO User'])
        if cdate == 'upload':
            res = UploadData.objects.filter(created__gte=start_date,created__lte=end_date, status='1').annotate(
            duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField())).annotate(
            duration1=ExpressionWrapper(F('action_date') - F('action_start_date'), output_field=DurationField()))
        else:
            res = UploadData.objects.filter(start_date__gte=start_date,start_date__lte=end_date, status='1').annotate(
                duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField())).annotate(
                duration1=ExpressionWrapper(F('action_date') - F('action_start_date'), output_field=DurationField()))
        rows = res.values_list('profile_id', 'name','dob','remarks', 'start_date', 'end_date', 'action_start_date', 'action_date',
                               'duration','duration1','picture1','picture_sc1','picture2','aremarks','matchcase','rating','altpicture1','altpicture_sc1','altscreen1','altaremarks1','altpicture2','altpicture_sc2','altscreen2','altaremarks2','user','hold_case','action','mlro_remarks','mlro_id')
        for user in rows:
            writer.writerow(user)

        return response

    return render(request, "home/report.html")

def rawreport(request):

    return render(request, "home/rawreport.html")

@login_required(login_url="/login/")
def rawreport_extract(request):
    if request.method == 'POST':
        start_date = datetime.strptime(request.POST['start_date'], "%m/%d/%Y").strftime('%Y-%m-%d')
        end_date = datetime.strptime(request.POST['end_date'], "%m/%d/%Y").strftime('%Y-%m-%d')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export_data.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['Profile Id', 'Name', 'Task Start Time', 'Task End Time', 'MLRO Start Time', 'MLRO End Time', 'Task Time', 'MLRO Time' ])

        res = UploadData.objects.filter(created__range=[start_date, end_date], status='1').annotate(
            duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField())).annotate(
            duration1=ExpressionWrapper(F('action_date') - F('action_start_date'), output_field=DurationField()))
        rows = res.values_list('profile_id', 'name', 'start_date', 'end_date', 'action_start_date', 'action_date',
                               'duration','duration1')
        for user in rows:
            writer.writerow(user)

        return response

    return render(request, "home/rawreport.html")



@login_required(login_url="/login/")
def break_add(request):
    return render(request, "home/break_add.html")

@login_required(login_url="/login/")
def action_take(request):
    user = request.user
    btn_val = request.POST.get('ActionStart')

    if request.method == 'POST':

        if btn_val == 'Add Break':
            exdata1 = AnalystLogs()
            exdata1.user_id = user.username
            exdata1.break_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exdata1.break_code = request.POST['brkcode']
            exdata1.break_chk = '0'
            exdata1.save()
            return HttpResponseRedirect(reverse('break_add'))
        elif btn_val == 'Start Task':
            exdata1 = AnalystLogs.objects.get(break_chk='0',user_id=user)
            exdata1.user_id = user.username
            exdata1.break_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exdata1.break_chk = '1'
            exdata1.save()
            return HttpResponseRedirect(reverse('feedback'))


@login_required(login_url="/login/")
def dashboard(request):
    objs1 = UploadData.objects.filter(picture1__exact='',status='1').annotate(
        time_elapsed=Sum(Cast(F('end_date') - F('start_date'), DurationField()))).aggregate(Avg('time_elapsed'))
    objs2 = UploadData.objects.exclude(picture1__exact='', status='1').annotate(
        time_elapsed=Sum(Cast(F('end_date') - F('start_date'), DurationField()))).aggregate(Avg('time_elapsed'))
    objs3 = UploadData.objects.filter(action='Approved', status='1').annotate(
        time_elapsed=Sum(Cast(F('action_date') - F('action_start_date'), DurationField()))).aggregate(Avg('time_elapsed'))
    objs = UploadData.objects.filter(status='1').annotate(
            duration=ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField()))
    count = UploadData.objects.all().count()

    totpic = 0
    totpicn = 0
    totappr = 0
    duratnot= str(objs1['time_elapsed__avg']).split(".")[0]
    durat = str(objs2['time_elapsed__avg']).split(".")[0]
    avgapprv = str(objs3['time_elapsed__avg']).split(".")[0]
    for item in objs:
        if item.picture1:
            totpic=totpic+1

        else:
            totpicn = totpicn + 1
        if item.action=='Approved':
            totappr=totappr+1


    totpof = totpic+totpicn
    unfill = count-totpof
    return render(request, "home/index.html",{'totpic':totpic,'totpicn':totpicn,'totpof':totpof,'totappr':totappr,'duratnot':duratnot,'durat':durat,'avgapprv':avgapprv,'unfill':unfill})

@login_required(login_url="/login/")
def similar_search1(request):
    if request.method == 'POST':
        name = request.POST['name']
        objs = UploadData.objects.filter(name__icontains=name, user__isnull=True)
    return render(request, "home/similar_search.html",{'objs':objs})
def similar_search(request):
    #print(str)
    if str is None:
        return render(request, "home/similar_search.html")
    else:
        objs = UploadData.objects.filter(name__icontains=str, user__isnull=True)

        print(objs)
        return render(request, "home/similar_search.html",{'objs':objs})

@login_required(login_url="/login/")
def apr(request):
    obj = None
    login = None
    logdata = []

    if request.method == 'POST':

        start_date = datetime.strptime(request.POST['start_date'], "%m/%d/%Y")
        end_date = datetime.strptime(request.POST['end_date'], "%m/%d/%Y")
        obj = UploadData.objects.raw("SELECT id,user,count(profile_id) cnt ,time(sum(ROUND((JULIANDAY(end_date) - JULIANDAY(start_date)) * 86400)), 'unixepoch') AS difference FROM upload_data where start_date not null and end_date is not null and date(start_date) BETWEEN date('"+str(start_date)+"') and date('"+str(end_date)+"') and ROUND((JULIANDAY(end_date) - JULIANDAY(start_date)) * 86400)<5000 group by user")
        #print(obj[2])
        #quit()
    #print(obj)
        for item in obj:
            item1 = {}
            item1['login'] = ''
            item1['id'] = item.id
            item1['user'] = item.user
            item1['cnt'] = item.cnt
            item1['difference'] = item.difference

            for lo in UserLogs.objects.raw("select user_logs.id,case when user_logs.event='Login' then min(user_logs.event_date) else '' END as login,p.logout,time(ROUND((JULIANDAY(p.logout) - JULIANDAY(case when user_logs.event='Login' then min(user_logs.event_date) else '' END)) * 86400),'unixepoch') totallogin,time(ROUND((JULIANDAY(time(ROUND((JULIANDAY(p.logout) - JULIANDAY(case when user_logs.event='Login' then min(user_logs.event_date) else '' END)) * 86400),'unixepoch')) - JULIANDAY('"+str(item.difference)+"')) * 86400),'unixepoch') totalbrk from user_logs join (select id,user_id,case when event='Logout' then max(event_date) else '' END as logout from user_logs where user_id='"+str(item.user)+"' and date(event_date)=date('"+str(start_date)+"')) p on user_logs.user_id=p.user_id where user_logs.user_id='"+str(item.user)+"' and date(user_logs.event_date)=date('"+str(end_date)+"')"):
                #print(lo.login)
                item1['login']=lo.login
                item1['logout'] = lo.logout
                item1['total'] = lo.totallogin
                item1['totalbrk'] = lo.totalbrk

            #for lo in UserLogs.objects.raw("select id,max(event_date) as login from user_logs where user_id='"+str(item.user)+"' and event='Logout' and date(event_date)=date('"+str(start_date)+"')"):
                #print(lo.login)
                #item1['logout']=lo.login
            logdata.append(item1)
    print(logdata)
    return render(request, "home/apr.html",{'obj':logdata})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
