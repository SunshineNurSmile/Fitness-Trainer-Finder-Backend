from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *

from base.models import Order, Trainee, Trainer

from base.serializers import OrderSerializer, TrainerSerializer

param_id = openapi.Parameter('id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
order_response = openapi.Response('response description', OrderSerializer)
orders_response = openapi.Response('response description', OrderSerializer(many=True))


# TODO
# Custom description and data type for swagger yaml
# example
# {
#     "_id": 5,
#     "orderItems": [
#         {
#             "_id": 6,
#             "name": "Yosuke",
#             "qty": 1,
#             "price": null,
#             "image": "/images/Screen_Shot_2022-02-24_at_8.58.09_PM.png",
#             "trainer": 5,
#             "order": 5
#         }
#     ],
#     "billingAddress": false,
#     "user": {
#         "id": 3,
#         "_id": 3,
#         "username": "foo2@test.com",
#         "name": "foo2",
#         "email": "foo2@test.com",
#         "first_name": "foo2",
#         "last_name": "bar2",
#         "isAdmin": false
#     },
#     "paymentMethod": "PayPal",
#     "taxPrice": "0.00",
#     "shippingPrice": "10.00",
#     "totalPrice": "10.00",
#     "paidAt": null,
#     "isDelivered": false,
#     "deliveredAt": null,
#     "createdAt": "2022-02-27T00:43:06.990429Z"
# }


@swagger_auto_schema(methods=['post'], request_body=OrderSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    # to get trainee from access token
    trainee_id = request.user.id
    trainee = Trainee.objects.get(_id=trainee_id)
    data = request.data
    trainer_id = request.data['trainer_id']
    trainer = Trainer.objects.get(_id=trainer_id)

    # try:
    order = Order.objects.create(
        trainee=trainee,
        trainer=trainer,
        paymentMethod=data['paymentMethod'],
        taxPrice=data['taxPrice'],
        totalPrice=data['totalPrice']
    )
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)
    # except:
    #     return Response(status=HTTP_400_BAD_REQUEST)



# TODO
# include above data example to swagger API
@swagger_auto_schema(methods=['get'], manual_parameters=[param_id], responses={200: order_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({'detail': 'No authorized to view this order'}, status=HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exists'}, status=HTTP_404_NOT_FOUND)


# TODO
@swagger_auto_schema(methods=['put'], manual_parameters=[param_id], responses={200: 'Order was paid'})
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)
    order.isPaid = True
    order.save()

    return Response('Order was paid')


@swagger_auto_schema(methods=['get'], responses={200: orders_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request,pk):
    obj = Trainee.objects.filter(_id=pk).first()
    order = obj.order_set.all()
    if order is None:
        return Response({'detail': 'Order does not exist'}, status=HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)


@swagger_auto_schema(methods=['get'], responses={200: trainers_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyTrainers(request, pk):
    a = []
    b = []
    obj = Order.objects.filter(trainee___id=pk).values('trainer')

    for i in obj:
        a.append(i['trainer'])
    Items = set(a)
    for i in Items:
        b.append(i)
    print(b)
    for i in b:
        trainer = Trainer.objects.filter().union(
            Trainer.objects.filter(_id=i)
        )
        if obj is None:
            return Response({'detail': 'Trainer does not exist'}, status=HTTP_404_NOT_FOUND)
    serializer = TrainerSerializer(trainer, many=True)
    return Response(serializer.data)



