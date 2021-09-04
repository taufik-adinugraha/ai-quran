from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import rekaman
from django.contrib.auth.models import User
from autentikasi.models import Profile
from django.db.models import Sum
from datetime import datetime
from django.conf import settings
from time import time
import numpy as np
import pandas as pd
import json
import os

# paths
INFO_DIR = settings.INFO_DIR
DATA_DIR = settings.DATA_DIR
AUDIO_DIR = settings.AUDIO_DIR

# info about surat & juz
info_juz = pd.read_csv(f'{DATA_DIR}/info_juz.csv')
with open(f'{INFO_DIR}/list_nama_surat.json', 'r') as f:
    data = f.read()
list_nama_surat = {i+1:v for i,v in enumerate(json.loads(data))}
# ayat quran
with open(f'{INFO_DIR}/all_ayat.json', 'r') as f:
    data = f.read()
all_ayat = json.loads(data)
# ayat quran simple
all_ayat_simple = pd.read_csv(f'{DATA_DIR}/quran-uthmani_simple.txt', sep='|', header=None)
all_ayat_simple.index = all_ayat_simple.apply(lambda x: f'{x[0]}_{x[1]}', axis=1)
all_ayat_simple = dict(all_ayat_simple[2])
# ayat quran simple no basmallah
all_ayat_simple_no_basmalah = pd.read_csv(f'{DATA_DIR}/quran_utsmani_no_basmalah.csv')
all_ayat_simple_no_basmalah.index = all_ayat_simple_no_basmalah.apply(lambda x: f'{x[0]}_{x[1]}', axis=1)
all_ayat_simple_no_basmalah = dict(all_ayat_simple_no_basmalah['2'])
# list name surat arab
with open(f'{INFO_DIR}/list_nama_surat_arab.json', 'r') as f:
    data = f.read()
list_nama_surat_arab = json.loads(data)
# list max ayat per surat
with open(f'{INFO_DIR}/max_ayat.json', 'r') as f:
    data = f.read()
max_ayat = json.loads(data)


@login_required(login_url="/login/")
def history(request, var):
    # var: variable to sort data (ayat, ukuran, waktu)
    db = rekaman.objects.filter(user=request.user.id).order_by('no_surat', 'no_ayat')
    if var == 'ukuran':
        db = rekaman.objects.filter(user=request.user.id).order_by('-ukuran')
    elif var == 'waktu':
        db = rekaman.objects.filter(user=request.user.id).order_by('-waktu')
    elif var in np.arange(1,115).astype('str'):
        db = rekaman.objects.filter(user=request.user.id, no_surat=int(var))        
    ndb = []
    for e in db:
        tmp = {
            'pk': e.pk,
            'no_surat': e.no_surat, 
            'no_ayat': e.no_ayat, 
            'no_surat__no_ayat': f'{e.no_surat}__{e.no_ayat}',
            'ukuran': e.ukuran//1000, 
            'waktu': e.waktu,
            'filepath': f'{settings.MEDIA_URL}{e.filename}',
            'nama_surat': list_nama_surat_arab[e.no_surat-1],
            'max_ayat': max_ayat[e.no_surat-1],
        }
        ndb.append(tmp)
    try:
        total_size = round(db.aggregate(Sum('ukuran'))['ukuran__sum']/1e6, 2)
    except:
        total_size = 0
    data = {
        'db': ndb,
        'total_ayat': db.count(),
        'total_ukuran': total_size,
        'segment': 'history',
    }
    # get selected surat (filter option)
    if var in np.arange(1,115).astype('str'):
        data.update({'selected_surat': list_nama_surat[int(var)]})
    else:
        data.update({'selected_surat': 'surat_ayat'})
    return render(request, 'history.html', data)


@login_required(login_url="/login/")
def delete_ayat(request, pk):
    if request.method == 'POST':
        dat = rekaman.objects.get(pk=pk)
        u = User.objects.get(username=dat.user)
        filename = dat.filename
        dat.delete()
        os.remove(f'{AUDIO_DIR}/{filename}')
    return redirect('history', 'surat_ayat')


@login_required(login_url="/login/")
def record(request, no_surat__no_ayat):
    if no_surat__no_ayat == '0':
        no_surat, no_ayat = 1, 1
    else:
        no_surat = int(no_surat__no_ayat.split('__')[0])
        no_ayat = int(no_surat__no_ayat.split('__')[1])
    data = {
        'no_surat': no_surat,
        'no_ayat': no_ayat,
        'segment': 'record',
    }     
    return render(request, 'record.html', data)


@login_required(login_url="/login/")
def upload(request):
    if request.method == 'POST':
        chars = 'abcdefghijklmnopqrstuvwxyz_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        filename = str(time()).replace('.','')[:12] + "".join([chars[i] for j in range(8) for i in np.random.randint(0,len(chars),1)]) + '.wav'
        with open(f'{AUDIO_DIR}/{filename}', 'wb') as file:
            file.write(request.body)
        data = request.headers['info'].split('_')
        print(data)
        b = User.objects.get(id=request.user.id)
        size = os.path.getsize(f'{AUDIO_DIR}/{filename}')
        try:
            # if data for particular "surat" & "ayat" already exist
            c = b.rekaman_set.get(no_surat=data[0], no_ayat=data[1])
            # delete old wav
            os.remove(f'{AUDIO_DIR}/{c.filename}')
            # update values
            c.ukuran = size
            c.filename = filename
            c.waktu = datetime.now()
            c.save()
        except:
            # new entry
            juz = info_juz[(info_juz['no_surat']==int(data[0])) & (info_juz['no_ayat']==int(data[1]))]['juz'].values[0]
            b.rekaman_set.create(no_surat=data[0], no_ayat=data[1], juz=juz ,ukuran=size, filename=filename)
        return redirect('history', 'surat_ayat')


def metadata_rekaman(request):
    # build dataframe from database
    df_ayat = pd.DataFrame(list(rekaman.objects.all().values()))
    df_user = pd.DataFrame(list(User.objects.all().values('id', 'username')))
    df_user =  df_user[df_user['username']!='admin']
    df_profile = pd.DataFrame(list(Profile.objects.all().values()))
    # merge df_user & df_profile
    df_user = df_user.merge(df_profile.drop(['id'], axis=1), how='left', left_on='id', right_on='user_id')
    df_user.drop(['user_id'], axis=1, inplace=True)
    # merge df_user & df_ayat
    df = df_user.merge(df_ayat.drop(['id'], axis=1), how='left', left_on='id', right_on='user_id')
    df.drop(['user_id'], axis=1, inplace=True)
    df.replace(np.nan, '', regex=True, inplace=True)
    return JsonResponse(df.to_dict())

def metadata_listSurat(request):
    return JsonResponse(list_nama_surat)

def metadata_listSuratArab(request):
    with open(f'{INFO_DIR}/list_nama_surat_arab.json', 'r') as f:
        data = f.read()
    obj = json.loads(data)
    return JsonResponse({i+1:v for i,v in enumerate(obj)})

def metadata_terjemah(request):
    with open(f'{INFO_DIR}/terjemah.json', 'r') as f:
        data = f.read()
    obj = json.loads(data)
    return JsonResponse(obj)

def metadata_maxAyat(request):
    with open(f'{INFO_DIR}/max_ayat.json', 'r') as f:
        data = f.read()
    obj = json.loads(data)
    return JsonResponse({i+1:v for i,v in enumerate(obj)})

def metadata_ayatQuran(request, surat_ayat):
    return JsonResponse(all_ayat[surat_ayat], safe=False)

def metadata_ayatQuranAll(request):
    return JsonResponse(all_ayat)

def metadata_ayatQuranSimple(request, surat_ayat):
    return JsonResponse(all_ayat_simple_no_basmalah[surat_ayat], safe=False)

def metadata_ayatQuranSimpleAll(request):
    return JsonResponse(all_ayat_simple)

def metadata_ayatQuranSimpleAllNoBasmalah(request):
    return JsonResponse(all_ayat_simple_no_basmalah)


@login_required(login_url="/login/")
def history_all_rekaman(request, lembaga_user):
    lembaga, user = lembaga_user.split('_')
    # build dataframe from database
    df_ayat = pd.DataFrame(list(rekaman.objects.all().values()))
    df_user = pd.DataFrame(list(User.objects.all().values('id', 'username')))
    df_user =  df_user[df_user['username']!='admin']
    df_profile = pd.DataFrame(list(Profile.objects.all().values()))
    # merge df_user & df_profile
    df_user = df_user.merge(df_profile.drop(['id'], axis=1), how='left', left_on='id', right_on='user_id')
    df_user.drop(['user_id'], axis=1, inplace=True)
    # merge df_user & df_ayat
    df = df_user.merge(df_ayat.drop(['id'], axis=1), how='left', left_on='id', right_on='user_id')
    df.drop(['user_id'], axis=1, inplace=True)
    # reset index
    df = df.set_index('id')

    # list kode lembaga
    list_lembaga = list(df.groupby('kode_lembaga')['kode_lembaga'].unique().index)
    # dict of user list
    user_dict = {}
    for l in list_lembaga:
        user_dict.update({l: list(set(df[df['kode_lembaga']==l]['username'].values))})
    
    user_id = df[df['username']==user].index[0]
    db = rekaman.objects.filter(user=user_id).order_by('no_surat', 'no_ayat')
    ndb = []
    for e in db:
        tmp = {
            'pk': e.pk,
            'no_surat': e.no_surat, 
            'no_ayat': e.no_ayat, 
            'filepath': f'{settings.MEDIA_URL}{e.filename}',
            'nama_surat': list_nama_surat_arab[e.no_surat-1],
            'max_ayat': max_ayat[e.no_surat-1],
        }
        ndb.append(tmp)
    try:
        total_size = round(db.aggregate(Sum('ukuran'))['ukuran__sum']/1e6, 2)
    except:
        total_size = 0
    data = {
        'list_lembaga': list_lembaga,
        'user_dict': user_dict,
        'selected_lembaga': lembaga,
        'selected_user': user,
        # 'selected_surat': list_nama_surat[int(surat)],
        'db': ndb,
        'total_ayat': db.count(),
        'total_ukuran': total_size,
        'segment': 'Allrecord',
    }

    return render(request, 'history_admin.html', data)
