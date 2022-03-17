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

from ..models import Trainee, Trainer

from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema

from ..serializers import TraineeSerializer, TrainerSerializer, UserSerializerWithToken, UserSerializerWithTrainee, \
    UserSerializerWithTrainer

param_id = openapi.Parameter('id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
user_trainee_response = openapi.Response('response description', UserSerializerWithTrainee)
user_trainer_response = openapi.Response('response description', UserSerializerWithTrainer)
trainee_response = openapi.Response('response description', TraineeSerializer)


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


class TraineeList(generics.ListAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
    permission_classes = [IsAdminUser]


class TrainerList(generics.ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAdminUser]


@swagger_auto_schema(methods=['post'], request_body=UserSerializerWithTrainee)
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
@swagger_auto_schema(methods=['get'], responses={200: user_trainee_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTrainee(request):
    user = request.user
    serializer = UserSerializerWithTrainee(user, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=TraineeSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTrainee(request):
    user = request.user
    data = request.data

    Trainee.objects.create(
        user=user,
        height=data['height'],
        weight=data['weight'],
        training_style=data['training_style'],
        dob=data['dob'],
        gender=data['gender'],
    )
    serializer = UserSerializerWithTrainee(user, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['put'], manual_parameters=[param_id], responses={201: 'Profile updated'})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateTrainee(request, pk):
    trainee = Trainee.objects.get(user_id=pk)

    data = request.data
    trainee.height = data['height']
    trainee.weight = data['weight']
    trainee.training_style = data['training_style']
    trainee.gender = data['gender']
    trainee.description = data['description']

    trainee.save()

    serializer = TraineeSerializer(trainee, many=False)

    return Response(serializer.data)


# TODO
# update response
@swagger_auto_schema(methods=['get'], responses={200: user_trainer_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTrainer(request):
    user = request.user
    serializer = UserSerializerWithTrainer(user, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=TrainerSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTrainer(request):
    user = request.user
    data = request.data

    Trainer.objects.create(
        user=user,
        price=data['price'],
        training_style=data['training_style'],
        description=data['description'],
        gender=data['gender'],
        dob=data['dob']
    )
    serializer = UserSerializerWithTrainer(user, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['put'], manual_parameters=[param_id], responses={201: 'Profile updated'})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateTrainer(request, pk):
    trainer = Trainer.objects.get(user_id=pk)

    data = request.data
    trainer.height = data['height']
    trainer.weight = data['weight']
    trainer.training_style = data['training_style']
    trainer.gender = data['gender']
    trainer.description = data['description']

    trainer.save()

    serializer = TrainerSerializer(trainer, many=False)

    return Response(serializer.data)


