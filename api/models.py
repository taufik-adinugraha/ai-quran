from django.db import models
from koleksi_data.models import rekaman

# Create your models here.
class FileUpload(models.Model):
	file = models.FileField(blank=False, null=False)
	rekaman_id = models.ForeignKey(rekaman, on_delete=models.CASCADE, related_name='rekaman', null=True, blank=True)

class CariAyatDS(models.Model):
	file = models.FileField(blank=False, null=False)
	result = models.CharField(blank=True, default='', max_length=1000)
	prediction = models.CharField(blank=True, default='', max_length=1000)
	
class CekHafalanDS(models.Model):
	file = models.FileField(blank=False, null=False)
	result = models.CharField(blank=True, default='', max_length=1000)
	prediction = models.CharField(blank=True, default='', max_length=1000)
	
class CekBacaanDS(models.Model):
	file = models.FileField(blank=False, null=False)
	result = models.CharField(blank=True, default='', max_length=1000)
	prediction = models.CharField(blank=True, default='', max_length=1000)