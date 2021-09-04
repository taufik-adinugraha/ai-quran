# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('record/<str:no_surat__no_ayat>/', views.record, name='record'),
    path('metadata/rekaman', views.metadata_rekaman, name='metadata_rekaman'),
    path('metadata/list_surat', views.metadata_listSurat, name='metadata_listSurat'),
    path('metadata/list_surat_arab', views.metadata_listSuratArab, name='metadata_listSuratArab'),
    path('metadata/terjemah', views.metadata_terjemah, name='metadata_terjemah'),
    path('metadata/max_ayat', views.metadata_maxAyat, name='metadata_maxAyat'),
    path('metadata/ayat_quran/<str:surat_ayat>/', views.metadata_ayatQuran, name='metadata_ayatQuran'),
    path('metadata/ayat_quran_all', views.metadata_ayatQuranAll, name='metadata_ayatQuranAll'),
    path('metadata/ayat_quran_simple/<str:surat_ayat>/', views.metadata_ayatQuranSimple, name='metadata_ayatQuranSimple'),
    path('metadata/ayat_quran_simple_all', views.metadata_ayatQuranSimpleAll, name='metadata_ayatQuranSimpleAll'),
    path('metadata/ayat_quran_simple_all_nobasmalah', views.metadata_ayatQuranSimpleAllNoBasmalah, name='metadata_ayatQuranSimpleAllNoBasmalah'),
    path('upload/', views.upload, name='upload'),
    path('history/<str:var>', views.history, name='history'),
    path('history/delete/<int:pk>/', views.delete_ayat, name='delete_ayat'),
    path('history_all_rekaman/<str:lembaga_user>/', views.history_all_rekaman, name='history_all_rekaman'),
]