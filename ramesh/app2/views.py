from django.shortcuts import render,redirect
from django.http import HttpResponse
# from .models import Destinations
from django.contrib.auth.models import User,auth
from django.contrib import messages
# from .models import Destinations

def login(request):
    
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username,password=password)
        if user  is not None:
            auth.login(request,user)
            # messages.info(request,'user Logined ')
            # return redirect('/')
            if user.is_superuser:
                return redirect('/panel/')  # Change to your desired admin page
            else:
                return redirect('/')  # Regular user home
        else:
            messages.info(request,'Invalid Credientials')
            return redirect('login')
        
    else:
        return render(request,'login.html')

def register(request):
    # return render("Hello world!")
    # data=Destinations.objects.all()
    # return render(request,'register.html')
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                print('User name alredy Exists')
                messages.info(request,'User name alredy Exists')
                return render(request, 'register.html', {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email,
                })
            elif User.objects.filter(email=email).exists():
                print('Email alredy Exists')
                messages.info(request,'Email alredy Exists')
                # return redirect('register')
                return render(request, 'register.html', {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email,
                })
            else:
                user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
                user.save()
                print('user created')
                # messages.info(request,'User Created Successafully,Login now!!!')
                # return redirect('register')
                return redirect('login')
                
        else:
            print('Password Not Matched')
            messages.info(request,'Password Not Matched Please Check !!!!!!!!!!!!')
            # return redirect('register')
            return render(request, 'register.html', {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'email': email,
                })
        
            
    else:
        return render(request,'register.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')
