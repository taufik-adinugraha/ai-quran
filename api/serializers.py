from rest_framework import serializers

from .models import CariAyatDS, CekHafalanDS, CekBacaanDS, FileUpload
from koleksi_data.models import rekaman

from autentikasi.models import Profile

from django.contrib.auth.models import User


class FileUploadSerializer(serializers.ModelSerializer):

	class Meta():
		model = FileUpload
		fields = ('file', 'rekaman_id')

class RekamanSerializer(serializers.ModelSerializer):
	
	rekaman = FileUploadSerializer(many=True)
	
	class Meta():
		model = rekaman
		fields = ('id', 'user', 'no_surat', 'no_ayat', 'juz', 'ukuran', 'filename', 'waktu', 'rekaman')

	def create(self, validated_data):
		filenames_data = validated_data.pop('rekaman')

		rek = rekaman.objects.create(**validated_data)

		for filename_data in filenames_data:
			file_obj = FileUpload.objects.create(rekaman_id=rek, **filename_data)

		return rek

	#def update(self, instance, validated_data):
	#	filenames_data = validated_data.pop('rekaman')
	#	filenames = (instance.rekaman).all()
	#	filenames = list(filenames)
	#	instance.user = validated_data.get('user', instance.user)
	#	instance.no_surat = validated_data.get('no_surat', instance.no_surat)
	#	instance.no_ayat = validated_data.get('no_ayat', instance.no_ayat)
	#	instance.save()
		
	#	for filename_data in filenames_data:
	#		filename = filenames.pop(0)
	#		filename.file = filename_data.get('file', filename.file)
	#		filename.save()
	#	return instance

	#def delete()
	
	
class CariAyatDSSerializer(serializers.ModelSerializer):
	class Meta():
		model = CariAyatDS
		fields = ('file', 'result', 'prediction')

class CekHafalanDSSerializer(serializers.ModelSerializer):
	class Meta():
		model = CekHafalanDS
		fields = ('file', 'result', 'prediction')

class CekBacaanDSSerializer(serializers.ModelSerializer):
	class Meta():
		model = CekBacaanDS
		fields = ('file', 'result', 'prediction')

class ProfileSerializer(serializers.ModelSerializer):
	class Meta():
		model = Profile
		fields = '__all__'
