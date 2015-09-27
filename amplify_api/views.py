import json
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from amplify_api.models import User, Group
from amplify_api.serializers import UserSerializer, GroupSerializer
from rest_framework import generics, status
import traceback

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

    def put(self, request, *args, **kwargs):
        data = request.data
        android_id = data['android_id']
        group = data['group']
        try:
            user = User.objects.get(pk=android_id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
        except:
            user = User.objects.create(android_id=android_id, group=group)
            user.save()
        return Response()

class GroupList(generics.ListCreateAPIView):
    """
    GET all the groups, or POST a group
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def post(self, request, *args, **kwargs):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT, or DELETE a group
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['POST'])
def create_group(request):
    try:
        if request.method == 'POST':
            data = request.data
        group_name = data['name']
        android_id = data['android_id']
        if group_name is None or android_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        group = Group.objects.create(name=group_name)
        group.save()
        # TODO: get the GCM token for the user and save it
        try:
            user = User.objects.get(android_id=android_id)
        except:
            user = User.objects.create(android_id=android_id, group=group, is_master=True)
        user.save()
        return Response(group.id)
    except:
        print '>>> traceback <<<'
        traceback.print_exc()
        print '>>> end of traceback <<<'

# WIll have to add more advanced features later


@api_view(['POST'])
def set_song(request):
    '''
    Sets the song for the group whenever the master plays a song.
    :param request:
    :return:
    '''
    data = request.data
    group = Group.objects.get(id=data['group'])
    group.song = data['song']
    # Start the slaves in 1 seconds
    group.master_start = datetime.now()
    group.slave_start = datetime.now() + timedelta(seconds=1.5)
    group.save()
    return Response(group.id)


@api_view(['GET'])
#TODO:
def get_song(request):
    '''
    The slaves constantly call this endpoint to see which song to play and when.
    :param request:
    :return:
    '''
    group=Group.objects.filter(id=request.GET['group'])[0]
    response_data = {}
    response_data["song"] = group.song
    response_data["start"] = unix_time_millis(group.slave_start)
    response_data["master_start"]=unix_time_millis(group.master_start)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_view(['GET'])
def stop_song(request):
    '''
    Master calls this endpoint when he pauses the song.
    :param request:
    :return:
    '''


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt.replace(tzinfo=None) - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0



