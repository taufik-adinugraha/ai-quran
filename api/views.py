from django.shortcuts import render

from scipy.io.wavfile import read
from deepspeech import Model
import pandas as pd
import json
import os
from time import time
import numpy as np

from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer, CariAyatDSSerializer, CekBacaanDSSerializer, CekHafalanDSSerializer, RekamanSerializer
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from django.contrib.auth.models import User

from django.conf import settings


# paths
BASE_DIR = settings.BASE_DIR
DATA_DIR = settings.DATA_DIR
AUDIO_DIR = settings.AUDIO_DIR

# info about surat & juz
info_juz = pd.read_csv(f'{DATA_DIR}/info_juz.csv')

# DeepSpeech Model
DSQ = Model(f'{BASE_DIR}/deepspeech/output_graph_imams_tusers_v2.pb')
DSQ.enableExternalScorer(f'{BASE_DIR}/deepspeech/quran.scorer')

# Text Quran Utsmani
df = pd.read_csv(f'{DATA_DIR}/quran_utsmani_no_basmalah.csv')
quran_dict = {f'{i[0]}_{i[1]}': i[2].split(' ') for i in df.values}

# search Ayat from quran_dict
def find_ayat(lookup):
    max_score = 0
    all_score = {}
    for key, value in quran_dict.items():
        score = 0
        for i in lookup:
            score += i in value
        match = score/len(value)
        all_score.update({key: (score, match)})
        if score > max_score:
            max_score = score
    if max_score > 0:
        result = { k:v for k, v in all_score.items() if v[0] == max_score }
    else:
        result = {}
    return result

# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def apiOverview(request):
	api_urls = {
	#'Upload':'/file-upload/',
	'Rekaman':'/rekaman-upload/',
	'Cari':'/cari-ayat/',
	#'Hafalan':'/cek-hafalan/',
	#'Bacaan':'/cek-bacaan/',
	}
	return Response(api_urls)
	
class RekamanView(APIView):
	#authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	
	parser_classes = (MultiPartParser, FormParser, )
	
	def post(self, request, format=None, *args, **kwargs):
		chars = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		filename = str(time()).replace('.','')[:12] + "".join([chars[i] for j in range(8) for i in np.random.randint(0,len(chars),1)]) + '.wav'
		request.FILES['file'].name = filename
		userid = self.request.user.id
		#user = User.objects.get(id=request.user.id)
		#username = self.request.user
		no_surat = self.request.data['no_surat']
		no_ayat = self.request.data['no_ayat']
		ukuran = self.request.FILES['file'].size
		
		juz = info_juz[(info_juz['no_surat']==int(no_surat)) & (info_juz['no_ayat']==int(no_ayat))]['juz'].values[0]
		
		data = {
			'user': userid,
			'no_surat': no_surat,
			'no_ayat': no_ayat,
			'juz': juz,
			'ukuran': ukuran,
			'filename': filename,
			'rekaman':[ {
				'file': request.FILES['file'],
			} ],
		}
		
		rekaman_serializer = RekamanSerializer(data=data)
		if rekaman_serializer.is_valid():
			rekaman_serializer.save()
			return Response(rekaman_serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(rekaman_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CariView(APIView):
	#permission_classes = [IsAuthenticated]
	permission_classes = [HasAPIKey|IsAuthenticated]
	
	parser_classes = (MultiPartParser, FormParser, )
	
	def get(self, request, format=None, *args, **kwargs):
		cari_ayat_ds_serializer = CariAyatDSSerializer(data=request.data)
		
		if cari_ayat_ds_serializer.is_valid():
			file_object = request.FILES['file']
			sr, signal = read(file_object)
			prediction = DSQ.stt(signal)
			result = find_ayat(prediction.split(' '))
			# sorting based on similarity (high --> low)
			result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
			resp = {
				'result': result,
				'prediction': prediction,
			}
			
			return Response(resp, status=status.HTTP_200_OK)
		else:
			return Response(cari_ayat_ds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CekBacaanView(APIView):
	#permission_classes = [IsAuthenticated]
	permission_classes = [HasAPIKey|IsAuthenticated]
	
	parser_classes = (MultiPartParser, FormParser, )
	
	def get(self, request, format=None, *args, **kwargs):
		cek_bacaan_ds_serializer = CekBacaanDSSerializer(data=request.data)
		
		if cek_bacaan_ds_serializer.is_valid():
			file_object = request.FILES['file']
			sr, signal = read(file_object)
			prediction = DSQ.stt(signal)
			result = find_ayat(prediction.split(' '))
			resp = {
				'result': result,
				'prediction': prediction,
				}
			return Response(resp, status=status.HTTP_200_OK)
		else:
			return Response(cari_ayat_ds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			
class CekHafalanView(APIView):
	#permission_classes = [IsAuthenticated]
	permission_classes = [HasAPIKey|IsAuthenticated]
	
	parser_classes = (MultiPartParser, FormParser, )
	
	def get(self, request, format=None, *args, **kwargs):
		cek_hafalan_ds_serializer = CekBacaanDSSerializer(data=request.data)
		
		if cek_hafalan_ds_serializer.is_valid():
			file_object = request.FILES['file']
			sr, signal = read(file_object)
			prediction = DSQ.stt(signal)
			result = find_ayat(prediction.split(' '))
			resp = {
				'result': result,
				'prediction': prediction,
				}
			return Response(resp, status=status.HTTP_200_OK)
		else:
			return Response(cari_ayat_ds_serializer.errors, status=status.HTTP_400_BAD_REQUEST)