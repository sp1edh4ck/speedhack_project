from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import CustomUser
from rest_framework import serializers, generics
from .serializers import CustomUserSerializer


@api_view(['GET'])
def get_user_through_tg_link(tg_username):
    user = CustomUser.objects.filter(tg_link=tg_username)
    serializer = CustomUserSerializer(user, many=True)
    return Response(serializer.data)


class GetUserThroughTgLink(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
