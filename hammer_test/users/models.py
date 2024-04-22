from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    entered_invite_code = models.CharField(max_length=6, blank=True, null=True)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='invited_users')
