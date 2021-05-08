from django.contrib.auth import authenticate, login, logout

from attendance.models import (User, AttendanceRequest, AttendanceResponse, Batch)
from .serializers import (LoginSerializer, TakeAttendanceSerializer, AttendanceResponseSerializer)

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from django.utils import timezone
import datetime


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
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAttendanceResponse(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AttendanceResponseSerializer

    def post(self, request, format=None):
        request.data._mutable = True
        # check if an attendance request with the given meet link is present or not
        try:
            attendance_request_obj = AttendanceRequest.objects.filter(meet_link=request.data['meet_link']).last()
        except:
            return Response("No such meeting link found", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        request.data.update({'attendance_request': attendance_request_obj.id})
        serializer = AttendanceResponseSerializer(data=request.data, partial=True)
        

        if serializer.is_valid():
            if(attendance_request_obj.created_at + datetime.timedelta(seconds=attendance_request_obj.response_time) > timezone.now()):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response("The attendance got expired",status=status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


