from django.shortcuts import render, redirect
from django.http import HttpResponse
from scipy.io.wavfile import read
from deepspeech import Model
from django.conf import settings
from django.http import JsonResponse
import pandas as pd
import json
import io
import os


# paths
BASE_DIR = settings.BASE_DIR
DATA_DIR = settings.DATA_DIR
INFO_DIR = settings.INFO_DIR

# DeepSpeech Model
DSQ0 = Model(f'{BASE_DIR}/deepspeech/model_1006211730-1024-taufik-E.pb')
DSQ = Model(f'{BASE_DIR}/deepspeech/model_1006211730-1024-taufik-E.pb')
DSQ.enableExternalScorer(f'{BASE_DIR}/deepspeech/quran.scorer')

# Text Quran Utsmani
df = pd.read_csv(f'{DATA_DIR}/quran_utsmani_no_basmalah.csv')
quran_dict = {f'{i[0]}_{i[1]}': i[2].split(' ') for i in df.values}

# List bacaan Non-Quran
# with open(f'{INFO_DIR}/list_baca.json', 'r') as f:
    # data = f.read()
f = open(f'{INFO_DIR}/list_baca.json', encoding="cp437")
data = f.read()
baca_arab = json.loads(data)

# search Ayat from quran_dict
def find_ayat(lookup):
    max_score = 0
    all_score = {}
    for key, target in quran_dict.items():

        # score = 0
        # for i in lookup:
        #     score += i in target

        match_words = []
        try:
            ref = target.index(lookup[0])
        except:
            continue
        for idx, x in enumerate(target):
            for idy, y in enumerate(lookup):
                if (x==y) & (idx-ref == idy):
                    match_words.append(x)
        score = len(match_words)

        match = score/len(target)
        all_score.update({key: (score, match)})
        if score > max_score:
            max_score = score
    if max_score > 0:
        result = { k:v for k, v in all_score.items() if v[0] == max_score }
    else:
        result = {}
    return result


def cari(request):
    data = {
        'segment': 'cari',
    }
    if request.method == 'POST':
        # audio recognition
        sr, signal = read(request.FILES['file'].file)
        prediction = DSQ.stt(signal)
        result = find_ayat(prediction.split(' '))
        # sorting based on similarity (high --> low)
        result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
        data = {
            'result': json.dumps(result),
            'prediction': prediction,
            'segment': 'cari',
        }        
        return HttpResponse(json.dumps(data), content_type='application/json')
    return render(request, 'cari.html', data)


def hafalan(request):
    data = {
        'segment': 'hafalan',
    } 
    if request.method == 'POST':
        # audio recognition
        sr, signal = read(request.FILES['file'].file)
        prediction = DSQ.stt(signal).split(' ')
        data = {
            'prediction': prediction,
            'segment': 'hafalan',
        }
        return HttpResponse(json.dumps(data), content_type='application/json')     
    return render(request, 'hafalan.html', data)


def bacaan(request):
    data = {
        'segment': 'bacaan',
    } 
    if request.method == 'POST':
        # audio recognition
        sr, signal = read(request.FILES['file'].file)
        prediction = DSQ0.stt(signal).split(' ')
        data = {
            'prediction': prediction,
            'segment': 'bacaan',
        }
        return HttpResponse(json.dumps(data), content_type='application/json')     
    return render(request, 'bacaan_non-quran.html', data)

def metadata_bacaNonQuran(request):
    return JsonResponse(baca_arab)  