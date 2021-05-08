from django.contrib.auth import authenticate, login, logout

from attendance.models import (User, AttendanceRequest, AttendanceResponse, Batch)
from .serializers import LoginSerializer

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

