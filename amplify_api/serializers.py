__author__ = 'nich'

from rest_framework import serializers
from models import User, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('android_id', 'group', 'is_master')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'song', 'master_start', 'slave_start')
