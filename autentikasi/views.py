from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from koleksi_data.models import rekaman
import json



# white list "Kode Lembaga"
with open(f'{settings.DATA_DIR}/white_list_lembaga.json', 'r') as f:
    data = f.read()
white_list_lembaga = json.loads(data)
# list max ayat per surat
with open(f'{settings.INFO_DIR}/max_ayat.json', 'r') as f:
    data = f.read()
max_ayat = json.loads(data)


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:    
                msg = 'username atau password tidak valid'    
        else:
            msg = 'form isian tidak tervalidasi'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg, "segment": "login"})



def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('kode_lembaga') not in white_list_lembaga:
                msg = 'lembaga tidak terdaftar'
            else:
                user = form.save()
                user.refresh_from_db()
                user.profile.kelamin = form.cleaned_data.get('kelamin')
                user.profile.kelompok_usia = form.cleaned_data.get('kelompok_usia')
                user.profile.kode_lembaga = form.cleaned_data.get('kode_lembaga')
                user.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)

                msg     = 'Akun berhasil dibuat - silakan <a href="/login">login</a>.'
                success = True
            
                #return redirect("/login/")
        else:
            msg = 'form tidak valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })



@login_required(login_url="/login/")
def profile(request):
    db = User.objects.get(username=request.user)
    if request.method == "POST":
        db.profile.kelamin = request.POST['kelamin']
        db.profile.kelompok_usia = request.POST['kelompok_usia']
        db.save()
        db = User.objects.get(username=request.user)
    # surat completeness
    percent_completeness = [round(len(rekaman.objects.filter(user=request.user.id, no_surat=i))/max_ayat[i-1]*100) for i in range(1, 115)]
    color_completeness = ['rgb(255, 127, 80, 0.7)' if i != 100 else 'rgba(64, 224, 208)' for i in percent_completeness]
    Nayat = len(rekaman.objects.filter(user=1))
    completeness = {'Nayat': Nayat, 'total_percent': round(Nayat/6236*100,2)}
    print(round(Nayat/6236,2))
    data = {
        'username': db.username,
        'email': db.email,
        'kelamin': db.profile.kelamin,
        'kelompok_usia': db.profile.kelompok_usia,
        'kode_lembaga': white_list_lembaga[db.profile.kode_lembaga],
        'percent_completeness': percent_completeness,
        'color_completeness': color_completeness,
        'completeness': completeness,
        'segment': 'profile',
    } 
    return render(request, 'profile.html', data)

