from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('autentikasi.urls')),
    path('', include('dashboard.urls')),
    path('', include('koleksi_data.urls')),
    path('', include('ayat_recog.urls')),
	path('api/', include('api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)