from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('queries', views.queries, name='queries'),
    path('bookings', views.bookings, name='bookings'),
    path('packages', views.packages, name='packages'),
    path('logout', views.logout, name='logout'),
    # path('register', views.register, name='register'),
    # path('logout', views.logout, name='logout'),
]
