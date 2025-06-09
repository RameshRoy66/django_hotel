from django.urls import path
from . import views


urlpatterns = [
    path('', views.members, name='members'),
    path('places', views.places, name='places'),
    path('packages', views.packages, name='packages'),
    path('details', views.details, name='details'),
    path('book', views.book_now, name='book_now'),  # Add this
    path('my_bookings', views.my_bookings, name='my_bookings'),
    path('sendemail', views.send_test_email, name='send_email'),
    path('contact_page', views.contact_page, name='contact_page'),
    path('submit-contact/', views.submit_contact, name='submit_contact'),

] 
