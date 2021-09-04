from django.urls import path, re_path
from . import views

urlpatterns = [
    path('cari/', views.cari, name='cari'),
    path('hafalan/', views.hafalan, name='hafalan'),
    path('bacaan/', views.bacaan, name='bacaan'),
    path('metadata_bacaNonQuran/', views.metadata_bacaNonQuran, name='metadata_bacaNonQuran'),
]