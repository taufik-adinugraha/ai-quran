# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]