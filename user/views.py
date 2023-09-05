from django.shortcuts import render
import requests
import json
from django.shortcuts import render
import datetime
from datetime import date
from codecs import ignore_errors
from functools import partial
from inspect import isfunction
from re import X

from django.db import DatabaseError, transaction
from django.db.models.aggregates import Max
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import *
from user.serializers import *


from decouple import Config, RepositoryEnv, Csv
DOTENV_FILE = './config/.env'
getenv = Config(RepositoryEnv(DOTENV_FILE))


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UserUpload(request):

    if request.method == 'GET':

        mymodels = users.objects.all()
        myserializer = UserSerializer(mymodels, many=True)
        
        formater = {
            "master": myserializer.data,
            "status": True
        }

        return JsonResponse({'message': 'successfully', 'results': formater},
                            status=201)

    if request.method == 'POST':
        try:
            localrequest = JSONParser().parse(request)
            mastermodel = users.objects.all()
            masterserializer = UserSerializer (
                mastermodel, data=localrequest)

            if masterserializer.is_valid():

                users_save = users(
                    email = localrequest["email"],
                    first_name = localrequest["first_name"],
                    last_name = localrequest["last_name"],
                    avatar = localrequest["avatar"],
                )
                users_save.save()

                mastermodel = users.objects.all()
                masterserializer = UserSerializer (
                    mastermodel, many=True)

                return JsonResponse({'message': 'successfully', 'results': masterserializer.data})
            return JsonResponse(masterserializer.errors, status=400)
        except users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def UserUpdate (request, pk):

    mymodels = users
    myserializer = UserSerializer 

    try:
        localmodel = mymodels.objects.get(id=pk)
    except mymodels.DoesNotExist:
        return JsonResponse({"result" : "unsuccessfully","status" : False,"message" : "id not found!!!"}, status=404)

    if request.method == 'GET':

        localserializer = myserializer(localmodel)
        localmodel = mymodels.objects.filter(id=pk)
        localserializer = myserializer(localmodel, many=True)

        return JsonResponse({"message": "successfully", "results": localserializer.data}, status=201)

    if request.method == 'PUT':
        try:
            localrequest = JSONParser().parse(request)

            check_error = users.objects.filter(id=pk).count()
            if check_error != 0:
                mastermodel = users.objects.get(id=pk)
                masterserializer = UserSerializer (
                    mastermodel, data=localrequest, partial=True)

                if masterserializer.is_valid():

                    masterserializer.save(
                        email = localrequest["email"],
                        first_name = localrequest["first_name"],
                        last_name = localrequest["last_name"],
                        avatar = localrequest["avatar"],
                    )

                return JsonResponse({"message": "successfully", "results": 'data has been change'}, status=200)
            else:
                return JsonResponse({"message": "unsuccessfully", "results": "id not found!!"}, status=400)
        except users.DoesNotExist:
            return JsonResponse({"message": "unsuccessfully", "results": "error"})

    elif request.method == 'DELETE':
        localmodel.delete()
        localmodel = mymodels.objects.filter(id=pk)
        localserializer = myserializer(localmodel, many=True)

    return JsonResponse({'message': 'successfully', 'status': True, 'count': 1, 'results': localserializer.data},
                        status=201)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteUser (request, pk):
    
    if request.method == 'DELETE':
        
        localmodel.delete()
        localmodel = users.objects.filter(id=pk)
        localserializer = UserSerializer(localmodel, many=True)
        
        formater = {
            "user" : localserializer.data,
        }

    return JsonResponse({'message': 'successfully', 'status': True, 'count': 1, 'results': formater}, 
                        status=201)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def UserFetch (request):
    
    if request.method == 'GET' :
        try :
            mastermodel = users.objects.all()
            masterserializer = UserSerializer(mastermodel, many=True)

            url = "https://reqres.in/api/users"
            print("GET Data")
            
            headers = {
                'Authorization': getenv('AUTHORIZATION'),
                'parameter' : 'page',
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers)
            datax = response.json()
            print(datax)
            
            if datax == 201:
    
                print('Save Data to database')
                print(datax)

                user_save = users(
                        id=mastermodel.id,
                        email=mastermodel.email,
                        first_name=mastermodel.first_name,
                        last_name=mastermodel.description,
                        avatar=mastermodel.avatar
                )
                user_save.save()
                    
            formater = {
                "master": masterserializer.data
            }

            return JsonResponse({'message': 'successfully', 'results': formater})
        except users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# @csrf_exempt
# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def UserFetch (request):
    
#     if request.method == 'GET' :
#         try :
#             # mymodels = users.objects.all()
#             # myserializer = UserSerializer (mymodels, many=True)
            
#             url = "https://reqres.in/api/users"
#             print("GET Data")
            
#             # payload = json.dumps({
#             #     "page": "1",
#             #     "per_page": "6",
#             #     "total": "12",
#             #     "total_pages": "2",
#             #     "users": {
#             #         "id": users.id,
#             #         "email": users.email,
#             #         "first_name": users.first_name,
#             #         "last_name": users.last_name,
#             #         "avatar": users.avatar,
#             #     },
#             #     "data": {
#             #         "id": "Body of Your User",
#             #         "email": "Title of Your User",
#             #         "first_name": "First name your user",
#             #         "last_name": "Last name your user",
#             #         "avatar": "Path of avatar image",
#             #     }
#             # })

#             headers = {
#                 'Authorization': getenv('AUTHORIZATION'),
#                 'parameter' : 'page',
#                 'Content-Type': 'application/json'
#             }
#             # response = requests.request(
#             #             "GET", url, headers=headers, data=payload)
#             response = requests.request("GET", url, headers=headers)
#             datax = response.json()
#             print(datax)
            
#             return JsonResponse({'message': 'successfully', 'results': url})
#         except users.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)