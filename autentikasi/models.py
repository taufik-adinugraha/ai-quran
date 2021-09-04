from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )
    kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES)
    AGE_GROUP = (
        ('A', '7-12'),
        ('B', '13-18'),
        ('C', '19-25'),
        ('D', '26-35'),
        ('E', '36-45'),
        ('F', '46-55'),
        ('G', '56+'),
    )
    kelompok_usia = models.CharField(max_length=5, choices=AGE_GROUP)
    kode_lembaga = models.CharField(max_length=6)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user = instance)



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()