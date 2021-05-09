from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from datetime import datetime


# Model for custom user
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=300)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# model for batches
class Batch(models.Model):
    name = models.CharField(max_length=50)
    batch_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_of_batch')
    meet_link = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name


# model for sending attendance request (for teachers)
class AttendanceRequest(models.Model):
    title = models.CharField(max_length=200)
    meet_link = models.URLField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_request_sender')
    response_time = models.IntegerField(default=120)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        request_name = self.sender.full_name +" "+ str(self.created_at)
        return request_name

# model for attendance response
class AttendanceResponse(models.Model):
    meet_link = models.URLField()
    email = models.EmailField()
    name = models.CharField(max_length=200, blank=True,null=True)
    attendance_request = models.ForeignKey(AttendanceRequest,on_delete=models.CASCADE, related_name='attendance_request_name')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    # class Meta:
    #     unique_together = ('email','attendance_request')


# model for sending notifications
class NotificationDetail(models.Model):
    meet_link = models.URLField()
    email = models.EmailField(unique=True)
    token1 = models.CharField(max_length=1500)
    token2 = models.CharField(max_length=1500)
    token3 = models.CharField(max_length=1500)

    def __str__(self):
        return self.email