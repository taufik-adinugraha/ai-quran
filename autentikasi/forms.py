# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))




class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Nama Akun",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control",
            }
        ))
    GENDER_CHOICES = (
        ('', ''),
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )
    kelamin = forms.CharField(
        widget = forms.Select(
            choices = GENDER_CHOICES,
            attrs={
                "placeholder" : "Jenis Kelamin",                
                "class": "form-control"
            }
        ))
    AGE_GROUP = (
        ('', ''),
        ('A', '7-12'),
        ('B', '13-18'),
        ('C', '19-25'),
        ('D', '26-35'),
        ('E', '36-45'),
        ('F', '46-55'),
        ('G', '56+'),
    )
    kelompok_usia = forms.CharField(
        widget=forms.Select(
            choices = AGE_GROUP,
            attrs={
                "placeholder" : "Kelompok Usia",                
                "class": "form-control"
            }
        ))    
    kode_lembaga = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Kode Lembaga",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'kelamin', 'kelompok_usia', 'kode_lembaga', 'password1', 'password2')




class UpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control",
            }
        ))
    GENDER_CHOICES = (
        ('', ''),
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )
    kelamin = forms.CharField(
        widget = forms.Select(
            choices = GENDER_CHOICES,
            attrs={
                "placeholder" : "Jenis Kelamin",                
                "class": "form-control"
            }
        ))
    AGE_GROUP = (
        ('', ''),
        ('A', '7-12'),
        ('B', '13-18'),
        ('C', '19-25'),
        ('D', '26-35'),
        ('E', '36-45'),
        ('F', '46-55'),
        ('G', '56+'),
    )
    kelompok_usia = forms.CharField(
        widget=forms.Select(
            choices = AGE_GROUP,
            attrs={
                "placeholder" : "Kelompok Usia",                
                "class": "form-control"
            }
        ))    

    class Meta:
        model = User
        fields = ('email', 'kelamin', 'kelompok_usia')