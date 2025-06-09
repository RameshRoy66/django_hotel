from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from app1.models import Queries
# Create your views here.

def home(request):
    return  render(request,'panel.html')


def queries(request):
    data = Queries.objects.select_related('user').all()
    return render(request, 'queries.html', {'data': data})


def bookings(request):
    return  render(request,'panel_booking.html')


def packages(request):
    return  render(request,'panel_packages.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
