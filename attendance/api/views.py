from django.contrib.auth import authenticate, login, logout

from attendance.models import (User, AttendanceRequest, AttendanceResponse, Batch, NotificationDetail)
from .serializers import (LoginSerializer, TakeAttendanceSerializer, AttendanceResponseSerializer,
                            NotificationObjectSerializer,)

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from mysite.settings import notification_sender_url

from django.utils import timezone
import datetime

import json
import requests


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = authenticate(request, username=request.data['email'], password=request.data['password'])
        # login(request, user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TakeAttendance(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TakeAttendanceSerializer

    def get(self, request, format=None):
        data = AttendanceRequest.objects.filter(sender=self.request.user.id)
        serializer = TakeAttendanceSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TakeAttendanceSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            receivers = NotificationDetail.objects.filter(meet_link=request.data['meet_link'])
            # list of all the token dictionary
            token_list = []
            
            for receiver in receivers:
                token_list_item = {}
                token_list_item["token1"]=receiver.token1
                token_list_item["token2"]=receiver.token2
                token_list_item["token3"]=receiver.token3
                token_list.append(token_list_item)
            

            headers={
                'content-type' : 'application/json'
            }

            body={
                'students': token_list
            }

            r = requests.post(notification_sender_url,headers=headers,data=json.dumps(body))

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAttendanceResponse(APIView):
    permission_classes = (permissions.AllowAny,)
    # serializer_class = AttendanceResponseSerializer

    def post(self, request, format=None):
        data = request.data
        # check if an attendance request with the given meet link is present or not
        try:
            attendance_request_obj = AttendanceRequest.objects.filter(meet_link=request.data['meet_link']).last()
        except:
            return Response("No such meeting link found", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        
        attendance_response_obj = AttendanceResponse(
            email=request.data['email'],
            meet_link=request.data['meet_link'],
            attendance_request=attendance_request_obj,
        )
        if(attendance_request_obj.created_at + datetime.timedelta(seconds=attendance_request_obj.response_time) > timezone.now()):
            attendance_response_obj.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response("The attendance got expired",status=status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateNotificationObject(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = NotificationObjectSerializer

    def post(self,request, format=None):
        serializer = NotificationObjectSerializer(data=request.data)
        try:
            obj = NotificationDetail.objects.get(email=request.data['email'])
            if obj is not None:
                obj.meet_link = request.data['meet_link']
                obj.token1 = request.data['token1']
                obj.token2 = request.data['token2']
                obj.token3 = request.data['token3']
                obj.save()
                return Response('Updated', status=status.HTTP_201_CREATED)

        except:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

