from django.conf import settings
from pathlib import Path
import pandas as pd
import json


# paths
BASE_DIR = settings.BASE_DIR
INFO_DIR = settings.INFO_DIR
DATA_DIR = settings.DATA_DIR
AUDIO_DIR = settings.AUDIO_DIR


# load info from files
info_juz = pd.read_csv(f'{DATA_DIR}/info_juz.csv')
info_surat = pd.read_csv(f'{DATA_DIR}/info_surat.csv')
terjemah = pd.read_csv(f'{DATA_DIR}/terjemah_edit.csv')
all_ayat = pd.read_csv(f'{DATA_DIR}/quran-uthmani.txt', sep='|', header=None)


# extract info
list_nama_surat = list(info_surat.apply(lambda x: f'{x[0]}. {x[2]} ({x[1]})', axis=1))
list_nama_surat_arab = list(info_surat.apply(lambda x: x[1], axis=1))
max_ayat = list(info_surat.apply(lambda x: x[3], axis=1))
terjemah.index = terjemah.apply(lambda x: f'{x[0]}_{x[1]}', axis=1)
terjemah = dict(terjemah['terjemah'])
all_ayat.index = all_ayat.apply(lambda x: f'{x[0]}_{x[1]}', axis=1)
all_ayat = dict(all_ayat[2])

# create json files
with open(f'{INFO_DIR}/list_nama_surat.json', 'w') as fp:
    json.dump(list_nama_surat, fp)
with open(f'{INFO_DIR}/list_nama_surat_arab.json', 'w') as fp:
    json.dump(list_nama_surat_arab, fp)
with open(f'{INFO_DIR}/terjemah.json', 'w') as fp:
    json.dump(terjemah, fp)
with open(f'{INFO_DIR}/all_ayat.json', 'w') as fp:
    json.dump(all_ayat, fp)
with open(f'{INFO_DIR}/max_ayat.json', 'w') as fp:
    json.dump(max_ayat, fp)