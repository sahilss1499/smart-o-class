from django.contrib.auth import authenticate, login, logout

from attendance.models import (User, AttendanceRequest, AttendanceResponse, Batch)
from .serializers import (LoginSerializer, TakeAttendanceSerializer)

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


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



