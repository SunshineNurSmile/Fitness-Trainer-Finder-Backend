from django.contrib.auth.models import User
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# from backend.base.models import UserProfile
from ..models import Order, OrderItem, Review, BillingAddress, Trainer, Trainee

# TODO - create Trainers

class UserSerializerWithTrainee(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    trainee = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'name', 'email', 'first_name', 'last_name', 'isAdmin', 'trainee']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name + ' ' + obj.last_name
        if name == '':
            name = obj.email

        return name

    def get_trainee(self, obj):
        serializer = TraineeSerializer(obj.trainee, many=False)
        return serializer.data


class UserSerializerWithToken(UserSerializerWithTrainee):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'name', 'email', 'first_name', 'last_name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class TraineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = '__all__'