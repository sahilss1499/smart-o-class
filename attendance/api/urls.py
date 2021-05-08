from django.urls import include, path
from .views import (LoginView, TakeAttendance)

urlpatterns = [
    path('login', LoginView.as_view()),
    path('take-attendance', TakeAttendance.as_view()),
]