from datetime import datetime, date

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import (UserRegisterForm, UserLoginForm, BatchCreationForm)
from .models import (User, AttendanceRequest, AttendanceResponse, Batch)

from django.contrib.auth import authenticate, login, logout

from django.core.exceptions import ValidationError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)

# Create your views here.
def index(request):
    return render(request,'base.html')




def UserLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    else:
        form = UserLoginForm()
        if request.method == 'POST':
            form = UserLoginForm(request.POST)

            if form.is_valid():
                password = request.POST.get('password')
                username = request.POST.get('email')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
        print("ok")    
        context = {'form': form}
        return render(request,'login.html',context)


@login_required(login_url='login')
def UserLogout(request):
    logout(request)
    return redirect('index')

def Register(request):
    if request.user.is_authenticated:
        return redirect('index')

    else:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
    
            if form.is_valid():
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                # print("ok")
                if password == confirm_password:
                    # print("ok")
                    user = User(
                        username = email,
                        email = email,
                        full_name= full_name,
                    )
                    print("ok")
                    user.set_password(password)
                    user.save()
                    return redirect('login')
                else:
                    print("passwords didn't match")
                    return redirect('register')
        
        context = {'form': form}
        return render(request, 'register.html',context)

        

# view list of batches of the teacher
class BatchListView(ListView,LoginRequiredMixin):
    model = Batch
    login_url = 'login'
    def get_queryset(self):
        return Batch.objects.filter(batch_admin=self.request.user.id)



# view for a teacher/ batch admin to add a batch
@login_required(login_url='login')
def CreateBatch(request):
    form = BatchCreationForm()

    if request.method == 'POST':
        form = BatchCreationForm(request.POST)

        if form.is_valid():
            print("ok")
            batch_name = request.POST.get('name')
            meet_link = request.POST.get('meet_link')
            batch_admin = User.objects.get(id=request.user.id)

            batch = Batch(
                name=batch_name,
                meet_link=meet_link,
                batch_admin=batch_admin,
            )
            batch.save()
            return redirect('batch_list')
        
    context = {'form': form}
    return render(request, 'batch_create.html', context)


# for viewing attendance date list inside a batch
@login_required(login_url='login')
def BatchAttendance(request, pk):
    batch = Batch.objects.get(id=pk)

    attendance_requests = AttendanceRequest.objects.filter(meet_link=batch.meet_link)

    date_set = set()

    for attendance_request in attendance_requests:
        date = attendance_request.created_at.date()
        yyyymmdd = date.strftime('%Y-%m-%d')
        date_set.add(f'{yyyymmdd}-{pk}')
    
    context = {'dates': date_set}
    return render(request,'date_list.html' ,context)


# for fetching attendance responses for a given date and time
@login_required(login_url='login')
def AttendanceResponseList(request,val):
    list = val.split('-')
    yyyy = list[0]
    mm = list[1]
    dd = list[2]

    batch_id = list[3]
    batch_obj = Batch.objects.get(pk=batch_id)

    attendance_qs = AttendanceResponse.objects.filter(meet_link=batch_obj.meet_link, created_at__date=date(int(yyyy),int(mm),int(dd)))
    total_attendance_requests = AttendanceRequest.objects.filter(
        meet_link=batch_obj.meet_link, created_at__date=date(int(yyyy),int(mm),int(dd))
    ).count()
    # to store email ids of responses
    email_ids = set()

    for attendance_response in attendance_qs:
        email_ids.add(attendance_response.email)

    # dictionary to store count of attendance responses fo a particular date email-wise
    attendance_count = {}

    for email_id in email_ids:
        attendance_count[email_id] = 0
    
    for attendance_response in attendance_qs:
        attendance_count[attendance_response.email] += 1
    
    for key, value in attendance_count.items():
        attendance_count[key] = (value/total_attendance_requests)*100
    
    print(total_attendance_requests)
    print(attendance_count)

    context = {'attendance_count': attendance_count}
    return render(request,'attendance_list.html', context)