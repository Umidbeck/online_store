from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profiles/', blank=False, null=False)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
