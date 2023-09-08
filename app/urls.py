# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path ,include
from app import views 
from django.conf.urls import url
from app import employee_views
from app.views import webhook

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path("booking/", include("booking.urls")),

    path('webhooks', webhook),

    re_path(r'^transactions/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.TransactionView.as_view(),
            name='transactions'),

    re_path(r'^customers/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.CustomerView.as_view(),
            name='customers'),

    re_path(r'^employee/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.employeeView.as_view(),
            name='employee'),



    

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
