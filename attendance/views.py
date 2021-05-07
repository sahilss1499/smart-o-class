from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import (UserRegisterForm, UserLoginForm)
from .models import (User)

from django.contrib.auth import authenticate, login, logout

from django.core.exceptions import ValidationError

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
            
        context = {'form': form}
        return render(request,'login.html',context)



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
                    user = User(
                        full_name= full_name,
                        email = email,
                    )
                    user.set_password(password)
                    user.save()
                    return redirect('login')
                else:
                    print("passwords didn't match")
                    return redirect('register')
        
        context = {'form': form}
        return render(request, 'register.html',context)

        
