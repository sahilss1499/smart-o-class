from attendance.models import User

from django.contrib.auth.models import auth

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed




class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=255, min_length=3, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = ['id','email','password']

    def validate(self,data):
        email = data['email']
        password = data['password']

        user_qs=User.objects.filter(email=email)
        if user_qs.exists():
            user = auth.authenticate(email=email, password=password)
            if not user:
                raise AuthenticationFailed({'error':'Invalid credentials, try again!'})
        
        else:
            raise serializers.ValidationError({'error':'User does not exists!'})
        
        return {'id': user.id, 'email': user.email}