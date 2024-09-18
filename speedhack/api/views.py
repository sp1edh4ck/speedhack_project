from rest_framework import generics, status
from rest_framework.response import Response

from users.models import CustomUser

from .serializers import CustomUserSerializer


class GetUsers(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class GetUser(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'



class GetUserTgLink(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'tg_link'
