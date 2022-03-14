from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from drf_yasg import openapi
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from base.models import UserProfile
from base.serializer import UserProfileSerializer, UserSerializer, UserSerializerWithToken

from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema

param_id = openapi.Parameter('id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
user_response = openapi.Response('response description', UserSerializer)
user_profile_response = openapi.Response('response description', UserProfileSerializer)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # get dict data
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password']),
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'This email already exits'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateUser(request, pk):
#     user = User.objects.get(id=pk)
#
#     data = request.data
#
#     user.first_name = data['name']
#     user.username = data['email']
#     user.email = data['email']
#     user.is_staff = data['isAdmin']
#
#     user.save()
#
#     serializer = UserSerializer(user, many=False)
#
#     return Response(serializer.data)

# TODO
# update response
@swagger_auto_schema(methods=['get'], responses={200: user_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProfile(request):
    user = request.user
    data = request.data

    user_profile = UserProfile.objects.create(
        user=user,
        height=data['height'],
        weight=data['weight'],
        training_style=data['training_style'],
        dob=data['dob'],
        gender=data['gender'],
    )
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['put', 'patch'], manual_parameters=[param_id], responses={201: 'Profile updated'})
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request, pk):
    user_profile = UserProfile.objects.get(user_id=pk)

    data = request.data
    user_profile.height = data['height']
    user_profile.weight = data['weight']
    user_profile.training_style = data['training_style']
    user_profile.dob = data['dob']
    user_profile.gender = data['gender']

    user_profile.save()

    serializer = UserProfileSerializer(user_profile, many=False)

    return Response(serializer.data)



