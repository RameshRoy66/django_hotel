from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from app1.models import Queries,Booking,Destinations
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden

# Create your views here.
def superuser_required(user):
    return user.is_superuser

@login_required
# @user_passes_test(superuser_required)
def home(request):
    if request.user.is_superuser:
    
        pending_count = Queries.objects.filter(Q(query_response__isnull=True) | Q(query_response='')).count()
        resolved_count = Queries.objects.exclude(Q(query_response__isnull=True) | Q(query_response='')).count()
        booking = Booking.objects.count()
        destinations = Destinations.objects.count()
        
        data = Booking.objects.all().order_by('-id')[:5]
        for d in data:
            try:
                d.place_price = Destinations.objects.get(id=d.place_id).price
            except Destinations.DoesNotExist:
                d.place_price = 'N/A'
        return render(request, 'panel.html', {
            'pending_count': pending_count,
            'resolved_count': resolved_count,
            'booking': booking,
            'destinations': destinations,
            'data':data
        })
    else:
        return redirect('/')


   
    # return  render(request,'panel.html')
@login_required
# @user_passes_test(superuser_required)
def queries(request):
    if request.user.is_superuser:
    
    
        if request.method=='POST':
            id = request.POST['queryId']
            responseText = request.POST['responseText']
            reponder_id = request.user.id
            responder_name = request.user.get_full_name()
            # Get the query object by id or return 404
            query = get_object_or_404(Queries, id=id)
            # Update fields
            query.query_response = responseText
            query.reponder_id = reponder_id
            query.responder_name = responder_name
            query.save()
            return redirect('queries')  # Use your URL name
        
        else:
            data = Queries.objects.all()
            return render(request, 'queries.html', {'data': data})
    else:
        return redirect('/')
        
        

@login_required
# @user_passes_test(superuser_required)
def bookings(request):
    if request.user.is_superuser:
    
        data = Booking.objects.all().order_by('-id')
        for d in data:
            try:
                d.place_price = Destinations.objects.get(id=d.place_id).price
            except Destinations.DoesNotExist:
                d.place_price = 'N/A'
        return  render(request,'panel_booking.html',{'data':data})
    else:
        return redirect('/')


@login_required
# @user_passes_test(superuser_required)
def packages(request):
    if request.user.is_superuser:

        if request.method=='POST':
            name = request.POST['name']
            image = request.FILES['image']
            description = request.POST['description']
            price = request.POST['price']
            days = request.POST['days']
            offer = 1 if request.POST.get('offer') == 'on' else 0  # FIXED LINE
            # return HttpResponse(f"Name: {name}, Image: {image}, Description: {description}, Price: {price}, Days: {days}, Offer: {offer}")
            destinations=Destinations.objects.create(
                    name=name,
                    image=image,
                    description=description,
                    price=price,
                    days=days,
                    offer=offer,
            )
            messages.add_message(request, messages.SUCCESS, 'Package Added Successfully', extra_tags='package')
            return redirect('packages')
            # return  render(request,'panel_packages.html')
        else:
            data=Destinations.objects.all().order_by('-id')
            return  render(request,'panel_packages.html',{'data':data})
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')
