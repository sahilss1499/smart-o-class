from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Batch)
admin.site.register(AttendanceRequest)
admin.site.register(AttendanceResponse)
admin.site.register(NotificationDetail)
