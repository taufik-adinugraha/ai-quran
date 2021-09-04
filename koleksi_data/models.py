from django.db import models
from django.contrib.auth.models import User
 

class rekaman(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	no_surat = models.IntegerField()
	no_ayat = models.IntegerField()
	juz = models.IntegerField()
	ukuran = models.IntegerField()
	filename = models.CharField(max_length=200)
	waktu = models.DateTimeField(auto_now_add=True)