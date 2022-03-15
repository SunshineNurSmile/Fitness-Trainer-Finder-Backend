from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from base.models import Trainer, Review
from base.serializers import ReviewSerializer, TrainerSerializer

param_keyword = openapi.Parameter('keyword', openapi.IN_QUERY, description="test manual param",
                                  type=openapi.TYPE_STRING)
param_page = openapi.Parameter('page', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_INTEGER)
param_id = openapi.Parameter('id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)
trainer_response = openapi.Response('response description', TrainerSerializer)
trainers_response = openapi.Response('response description', TrainerSerializer(many=True))


@swagger_auto_schema(methods=['get'], manual_parameters=[param_keyword, param_page], responses={200: trainers_response})
@api_view(['GET'])
def getTrainers(request):
    query = request.query_params.get('keyword')
    if query is None:
        query = ''

    trainers = Trainer.objects.filter(
        first_name__icontains=query).order_by('-createdAt')
    # TODO search both first and last
    # trainers += Trainer.objects.filter(
    #     last_name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(trainers, 5)

    try:
        trainers = paginator.page(page)
    except PageNotAnInteger:
        trainers = paginator.page(1)
    except EmptyPage:
        trainers = paginator.page(paginator.num_pages)

    if page is None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = TrainerSerializer(trainers, many=True)
    return Response({'trainers': serializer.data, 'page': page, 'pages': paginator.num_pages})


@swagger_auto_schema(methods=['get'], manual_parameters=[param_id], responses={200: trainer_response})
@api_view(['GET'])
def getTrainerById(request, pk):
    trainer = Trainer.objects.get(_id=pk)
    serializer = TrainerSerializer(trainer, many=False)
    return Response(serializer.data)


@swagger_auto_schema(methods=['get'], manual_parameters=[param_id], responses={200: trainers_response})
@api_view(['GET'])
def getTopTrainers(request):
    trainers = Trainer.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = TrainerSerializer(trainers, many=True)
    return Response(serializer.data)


@swagger_auto_schema(methods=['put', 'patch'], manual_parameters=[param_id], responses={200: 'Image was uploaded'})
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
# TODO
# make sure this image can upload
def uploadImage(request):
    pass


@swagger_auto_schema(methods=['delete'], manual_parameters=[param_id])
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteTrainer(request, pk):
    trainer = Trainer.objects.get(_id=pk)
    trainer.delete()
    return Response({'Trainer delete'})


@swagger_auto_schema(methods=['post'], manual_parameters=[param_id], request_body=ReviewSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTrainerReview(request):
    data = request.data
    user = request.user
    trainer = request.trainer

    if trainer.review_set.filter(user=user).exits():
        return Response({'detail': 'This trainer is already reviewed'})

    elif data['rating'] is None:
        return Response({'detail': 'Please select rating'})

    else:
        review = Review.objects.create(
            user=user,
            trainer=trainer,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        reviews = trainer.review_set.all()
        trainer.numReviews = len(reviews)

        rating = sum(reviews)/len(reviews)
        trainer.rating = rating
        trainer.save()

        return Response({'Review Add'})

