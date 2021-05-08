from django.urls import include, path, register_converter
from .views import *

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('',index, name='index'),
    path('login',UserLogin, name='login'),
    path('logout',UserLogout, name='logout'),
    path('register',Register, name='register'),
    path('batches',BatchListView.as_view(), name='batch_list'),
    path('batches/<int:pk>',BatchAttendance,name='batch_attendance'),
    path('batches/<slug:val>',AttendanceResponseList, name='attendance_response_list'),
    path('create-batch', CreateBatch, name='create_batch')
    # path('batches/<int:pk>/<int:day>/<int:month>/<int:year>',AttendanceResponseList, name='attendance_response_list'),
]