import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from amplify_api.models import User, Group
from amplify_api.serializers import UserSerializer, GroupSerializer
from rest_framework import generics, status


class UserList(generics.ListCreateAPIView):
    """
    GET all the users, or POST a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT, or DELETE a user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListCreateAPIView):
    """
    GET all the groups, or POST a group
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT, or DELETE a group
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['POST'])
def create_group(request):
    if request.method == 'POST':
        data = request.data
    group_name = data['name']
    oauth = data['oauth']
    if group_name is None or oauth is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    group = Group.objects.create(name=group_name)
    group.save()
    user = User.objects.create(oauth=oauth, is_master=True)
    user.save()
    return Response(group.id)

# WIll have to add more advanced features later

@api_view(['POST'])
def set_song(request):
    data = request.data
    group = Group.objects.filter(id=data['group'])[0]
    group.song = data['song']
    # Start the slaves in 1 seconds
    group.master_start = datetime.now()
    group.slave_start = datetime.now() + timedelta(seconds=1.5)
    group.save()
    return Response(group.id)


@api_view(['GET'])
#TODO:
def get_song(request):
    group=Group.objects.filter(id=request.GET['group'])[0]
    response_data = {}
    response_data["song"] = group.song
    response_data["start"] = unix_time_millis(group.slave_start)
    response_data["master_start"]=unix_time_millis(group.master_start)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt.replace(tzinfo=None) - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0



