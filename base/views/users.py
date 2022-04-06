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
from rest_framework.status import *

from ..models import Trainee, Trainer, Order, Chat, Note

from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema

from ..serializers import TraineeSerializer, TrainerSerializer, UserSerializerWithToken, UserSerializerWithTrainee, \
    UserSerializerWithTrainer, ChatSerializer, NoteSerializer

param_id = openapi.Parameter('id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
user_trainee_response = openapi.Response('response description', UserSerializerWithTrainee)
user_trainer_response = openapi.Response('response description', UserSerializerWithTrainer)
trainee_response = openapi.Response('response description', TraineeSerializer)
trainees_response = openapi.Response('response description', TraineeSerializer(many=True))


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


class AllTraineesList(generics.ListAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer
    permission_classes = [IsAuthenticated]


class AllTrainersList(generics.ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAuthenticated]


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
        heightft=data['heightft'],
        heightin=data['heightin'],
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
    trainee.heightft = data['heightft']
    trainee.heightin = data['heightin']
    trainee.weight = data['weight']
    trainee.training_style = data['training_style']
    trainee.gender = data['gender']
    trainee.description = data['description']
    trainee.avatar = data['avatar']

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
        training_style=data['training_style'],
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
    trainer.avatar = data['avatar']
    trainer.image1 = data['image1']
    trainer.image2 = data['image2']
    trainer.image3 = data['image3']
    trainer.image4 = data['image4']
    trainer.image5 = data['image5']
    trainer.image6 = data['image6']
    trainer.image7 = data['image7']
    trainer.image8 = data['image8']
    trainer.image9 = data['image9']
    trainer.video = request.FILES.get('video')

    trainer.save()

    serializer = TrainerSerializer(trainer, many=False)

    return Response(serializer.data)


@swagger_auto_schema(methods=['get'], responses={200: trainees_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyTrainees(request):
    trainer_id = request.user.trainer.pk
    obj = Order.objects.filter(trainer=trainer_id).values('trainee')
    list_trainees = list(set([ i['trainee'] for i in obj ]))
    print(list_trainees)
    for i in list_trainees:
        trainee = Trainee.objects.filter().union(
            Trainee.objects.filter(_id=i)
        )
        if obj is None:
            return Response({'detail': 'Trainee does not exist'}, status=HTTP_404_NOT_FOUND)
    serializer = TraineeSerializer(trainee, many=True)

    return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=ChatSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createChat(request):
    # to get trainee from access token
    trainee_id = request.user.id
    trainee = Trainee.objects.get(_id=trainee_id)
    data = request.data
    trainer_id = request.data['trainer_id']
    trainer = Trainer.objects.get(_id=trainer_id)

    # try:
    chat = Chat.objects.create(
        trainee=trainee,
        trainer=trainer,
        chat_message=data['chat_message'],
    )
    serializer = ChatSerializer(chat, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['post'], request_body=ChatSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createNote(request):
    # to get trainee from access token
    trainee_id = request.user.id
    trainee = Trainee.objects.get(_id=trainee_id)
    data = request.data
    trainer_id = request.data['trainer_id']
    trainer = Trainer.objects.get(_id=trainer_id)

    # try:
    note = Note.objects.create(
        trainee=trainee,
        trainer=trainer,
        note_message=data['note_message'],
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['put'], manual_parameters=[param_id], responses={200: 'Notification Accepted!'})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateChatAccepted(request, pk):
    chat = Chat.objects.get(_id=pk)
    chat.isAccepted = True
    chat.save()

    return Response('Notification Accepted!')


@swagger_auto_schema(methods=['get'], responses={200: trainees_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyAcceptedTrainees(request):
    trainer_id = request.user.trainer.pk
    obj = Chat.objects.filter(isAccepted=True).filter(trainer=trainer_id).values('trainee')
    list_trainees = list(set([ i['trainee'] for i in obj ]))
    print(list_trainees)
    for i in list_trainees:
        trainee = Trainee.objects.filter().union(
            Trainee.objects.filter(_id=i)
        )
        if obj is None:
            return Response({'detail': 'The Accepted trainee does not exist'}, status=HTTP_404_NOT_FOUND)
    serializer = TraineeSerializer(trainee, many=True)

    return Response(serializer.data)




