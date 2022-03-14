from django.contrib.auth.models import User
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# from backend.base.models import UserProfile
from .models import Order, OrderItem, Review, BillingAddress, Trainer, Trainee
from .serializers.users import TraineeSerializer


class TrainerSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Trainer
        fields = '__all__'

    def get_reviews(self, obj):
        # TODO review
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    BillingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_BillingAddress(self, obj):
        try:
            address = BillingAddressSerializer(obj.billing_address, many=False)
        except:
            address = False
        return address

    def get_user(self, obj):
        trainee = obj.user.trainee
        serializer = TraineeSerializer(trainee, many=False)
        return serializer.data


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'


