from django.urls import include, path
from .views import (LoginView, TakeAttendance, StudentAttendanceResponse,
                    CreateNotificationObject,)

urlpatterns = [
    path('login', LoginView.as_view()),
    path('take-attendance', TakeAttendance.as_view()),
    path('attendance-response', StudentAttendanceResponse.as_view()),
    path('subscribe', CreateNotificationObject.as_view()),
]