from django.urls import include, path
from .views import (LoginView, TakeAttendance, StudentAttendanceResponse)

urlpatterns = [
    path('login', LoginView.as_view()),
    path('take-attendance', TakeAttendance.as_view()),
    path('attendance-response', StudentAttendanceResponse.as_view()),
]