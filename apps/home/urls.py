# -*- encoding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from apps.home import views,image_aws

urlpatterns = [

    # The home page
    #path('index', views.index, name='index'),
    path('upload_data', views.upload_data, name='upload_data'),
    path('', views.index, name='home'),
    path('feedback', views.feedback, name='feedback'),
    path('feedback_update', views.feedback_update, name='feedback_update'),
    path('details', views.details, name='details'),
    path('details_view', views.details_view, name='details_view'),
    path('details_view_update', views.details_view_update, name='details_view_update'),

    path('rej_details', views.rej_details, name='rej_details'),
    #path('rej_details_view', views.rej_details_view, name='rej_details_view'),
    #path('rej_details_view_update', views.rej_details_view_update, name='rej_details_view_update'),
    path('rej_details_view/<str>', views.rej_details_view, name='rej_details_view'),
    path('rej_details_view_update/', views.rej_details_view_update, name='rej_details_view_update'),

    path('report', views.report, name='report'),
    path('report_extract', views.report_extract, name='report_extract'),

    path('rawreport', views.rawreport, name='rawreport'),
    path('rawreport_extract', views.rawreport_extract, name='rawreport_extract'),
    path('index', views.dashboard, name='index'),
    path('image_aws', image_aws.upload_image, name='image_aws'),
    path('similar_search', views.similar_search, name='similar_search'),
    #path('similar_search1/<str>', views.similar_search1, name='similar_search'),
    path('similar_search1', views.similar_search1, name='similar_search'),
    path('break_add', views.break_add, name='break_add'),
    path('action_take', views.action_take, name='action_take'),
    path('apr', views.apr, name='apr'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
