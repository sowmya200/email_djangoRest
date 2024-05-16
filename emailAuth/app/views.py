from django.shortcuts import render

# Create your views here.
# views.py

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
# Assuming you're using the built-in User model
from rest_framework.decorators import api_view 
import random
import string
from app.models import OTP  # Assuming you have a model named OTP in your app

from django.core.exceptions import ValidationError

@api_view(['POST'])
@csrf_exempt
def send_otp(request):
    try:
        email = request.data.get('email')

        # Simple check to verify if the email is in a valid format
        if not '@' in email or '.' not in email:
            raise ValidationError("Invalid email format")

        # Perform basic validation on the email address
        if not email.endswith('@gmail.com'):
            raise ValidationError("Invalid email domain")

        # Generate OTP (a 6-digit code)
        otp = ''.join(random.choices(string.digits, k=6))

        # Send OTP to the user's email
        send_mail(
            'Your OTP',
            f'Your OTP is: {otp}',
            'sowmyakumaravel2024@gmail.com',  # Sender's email address
            [email],  # Recipient's email address
            fail_silently=False,
        )

        return JsonResponse({'message': 'OTP sent successfully'})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        error_message = f'An error occurred while sending OTP: {str(e)}'
        return JsonResponse({'error': error_message}, status=500)

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp_entered = request.data.get('otp')
    user = get_object_or_404(User, email=email)

    # Retrieve the most recent OTP instance for the user
    otp_instance = OTP.objects.filter(user=user).order_by('-timestamp').first()

    if otp_instance and otp_instance.otp == otp_entered:
        # OTP matched, proceed with further authentication or actions
        return JsonResponse({'message': 'OTP verified successfully'})
    else:
        # Invalid OTP
        return JsonResponse({'error': 'Invalid OTP'}, status=400)
