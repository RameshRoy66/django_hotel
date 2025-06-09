from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Destinations
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Booking, Destinations
from django.utils import timezone
from django.core.mail import send_mail


def members(request):
    # if request.user.is_authenticated:
        # return redirect('/')
    # return render("Hello world!")
        # data=Destinations.objects.all()
        data = Destinations.objects.filter(offer=True)
        return render(request,'landing.html',{'data':data})
    # else:
        # return redirect('login')


def places(request):
    # places = [
    #     {'name': 'Paris', 'description': 'The City of Lights.', 'image': 'https://images.unsplash.com/photo-1491553895911-0055eca6402d'},
    #     {'name': 'Bali', 'description': 'Tropical paradise with beaches.', 'image': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb'},
    #     {'name': 'Tokyo', 'description': 'Fusion of tradition and tech.', 'image': 'https://images.unsplash.com/photo-1505678261036-a3fcc5e884ee'},
    # ]
    data=Destinations.objects.all()
    return render(request, 'places.html', {'data': data})

def packages(request):
    packages = [
        {'name': 'Europe Tour', 'details': 'Paris, Rome, Amsterdam with hotels.', 'price': 999},
        {'name': 'Bali Escape', 'details': '5 nights villa + tours.', 'price': 699},
        {'name': 'NYC Weekend', 'details': 'Hotel + Broadway + sightseeing.', 'price': 499},
    ]
    return render(request, 'packages.html', {'packages': packages})


def details(request):
    id = request.GET.get('id')
    data = get_object_or_404(Destinations, id=id)
    return render(request, 'details.html', {'data': data})


def book_now(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        destination = get_object_or_404(Destinations, id=id)
        if request.method == 'POST':
            user_id = request.POST['uid']
            place_id = request.POST['pid']
            place = request.POST['p_name']
            date = request.POST['travel_date']
            days = request.POST['days']
            notes = request.POST['notes']
            created_date = timezone.now()
            # Save or send booking info here
             # Save data to the database
            booking=Booking.objects.create(
                user_id=user_id,
                place=place,
                place_id=place_id,
                date=date,
                days=days,
                notes=notes,
                created_date=created_date
            )
             # Send confirmation email
            # send_mail(
            #     subject='Booking Confirmed!',
            #     message=f"Hello {request.user.username},\n\nYour booking to {place} on {date} for {days} days has been successfully confirmed.\n\nThank you for choosing us!",
            #     from_email='venkatrameshgaraga66@gmail.com',
            #     recipient_list=[request.user.email],  # Make sure the user has a valid email
            #     fail_silently=False,
            # )
            subject = '🎉 Booking Confirmed - Thank You for Choosing Us!'

            message = f"""
            Hello {request.user.username},

            Your booking to {place} on {date} for {days} days has been successfully confirmed.

            Thank you for choosing us!
            """

            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f7f7f7;
                    padding: 20px;
                    color: #333;
                }}
                .email-container {{
                    background-color: #ffffff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    max-width: 600px;
                    margin: auto;
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                }}
                .header img {{
                    max-width: 150px;
                }}
                .content {{
                    font-size: 16px;
                    line-height: 1.6;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 13px;
                    color: #999;
                }}
                </style>
            </head>
            <body>
                <div class="email-container">
                <div class="header">
                    <h2>🌍 Ramesh Travels</h2>
                </div>
                <div class="content">
                    <p>Hello <strong>{request.user.username}</strong>,</p>
                    <p>🎫 Your booking to <strong>{place}</strong> on <strong>{date}</strong> for <strong>{days} days</strong> has been successfully <span style="color:green;"><strong>confirmed</strong></span>.</p>
                    <p>We’re excited to have you on board. Prepare for an amazing travel experience!</p>
                    <p>🧳 Safe travels,<br>Team Durga Travels</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from Ramesh Travels.</p>
                </div>
                </div>
            </body>
            </html>
            """

            send_mail(
                subject=subject,
                message=message,  # fallback + text
                from_email='venkatrameshgaraga66@gmail.com',
                recipient_list=[request.user.email],
                fail_silently=False,
                html_message=html_message  # <-- key line to make it beautiful
            )
            # return render(request, 'booking_success.html', {'destination': destination, 'date': booking.date})
            # messages.success(request, "Booking successful! Confirmation email sent.")
            return redirect('my_bookings')

        return render(request, 'book_now.html', {'destination': destination})
    else:
        messages.info(request,'please  Login To Continue')
        return redirect('login')


def my_bookings(request): 
    if request.user.is_authenticated: 
        bookings = Booking.objects.filter(user_id=request.user.id).order_by('-id')

        # Attach destination details to each booking
        for b in bookings:
            try:
                b.destination = Destinations.objects.get(id=b.place_id)
            except Destinations.DoesNotExist:
                b.destination = None  # handle case where place_id is invalid
        
        return render(request, 'my_bookings.html', {'bookings': bookings}) 
    else: 
        messages.warning(request, "Please login to view your bookings.") 
        return redirect('login')



def send_test_email(request):
    send_mail(
        subject='Test Email from Django',
        message='This is a test email sent using Gmail SMTP.',
        from_email='venkatrameshgaraga66@gmail.com',
        recipient_list=['spiderman630036@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent successfully!")


def contact_page(request):
    return render(request, 'contact.html')

def submit_contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        # Handle saving to DB or sending email here
        messages.success(request, 'Thanks for contacting us! We’ll get back to you soon.')
        return redirect('contact')