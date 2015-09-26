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

@api_view(['POST'])
def play(request):
    return None