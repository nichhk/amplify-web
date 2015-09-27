
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime

from rest_framework.authtoken.models import Token
from django.conf import settings

class Group(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, default='', unique=True)
    song = models.CharField(max_length=100, blank=True, default='')

    master_start = models.DateTimeField(blank=True, null=True)
    slave_start = models.DateTimeField(blank=True, null=True)



class UserManager(BaseUserManager):
    def _create_user(self, android_id, gcm_token, oauth, group, is_master):
        user = self.model(
            android_id=android_id,
            gcm_token=gcm_token,
            oauth=oauth,
            group=group,
            is_master=is_master,
        )
        user.save()
        return user

    def create_user(self, oauth, group, is_master):
        return self._create_user(oauth, group, is_master)

    def create_superuser(self, oauth, group, is_master):
        return self._create_user(oauth, group, is_master)

class User(AbstractBaseUser):
    created = models.DateTimeField(auto_now_add=True)
    android_id = models.CharField(max_length=100, blank=False, default='', primary_key=True)
    # oauth = models.CharField(max_length=200, blank=True, default='')
    group = models.ForeignKey("Group", null=True)
    is_master = models.BooleanField(default=False)
    gcm_token = models.CharField(max_length=100, blank=True, default='', null=True)

    USERNAME_FIELD = 'oauth'
    objects = UserManager()

    class Meta:
        ordering = ('created',)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)