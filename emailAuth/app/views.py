
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view 
import random
import string
from django.conf import settings
from .models import OTP
from datetime import timedelta
from django.utils import timezone


from django.core.exceptions import ValidationError

@api_view(['POST'])
@csrf_exempt
def send_otp(request):
    try:
        email = request.data.get('email')

        if not '@' in email or '.' not in email:
            raise ValidationError("Invalid email format")

        if not email.endswith('@gmail.com'):
            raise ValidationError("Invalid email domain")

        otp = ''.join(random.choices(string.digits, k=6))
        otp_instance = OTP.objects.create(email=email, otp=otp)

        expiry_time = timezone.now() + timedelta(minutes=5)
        otp_instance.expiry_time = expiry_time
        otp_instance.save()

        # Send OTP to the user's email
        send_mail(
            'Your OTP',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST,  # Sender's email address
            [email],  # Recipient's email address
            fail_silently=False,
        )

        return JsonResponse({'message': 'OTP sent successfully', 'otp': otp})

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        error_message = f'An error occurred while sending OTP: {str(e)}'
        return JsonResponse({'error': error_message}, status=500)

# @api_view(['POST'])
# def verify_otp(request):
#     email = request.data.get('email')
#     otp_entered = request.data.get('otp')
#     user = get_object_or_404(User, email=email)

#     otp_instance = OTP.objects.filter(user=user).order_by('-timestamp').first()

#     if otp_instance and otp_instance.otp == otp_entered:
#         return JsonResponse({'message': 'OTP verified successfully'})
#     else:
#         return JsonResponse({'error': 'Invalid OTP'}, status=400)
@api_view(['POST'])
@csrf_exempt
def verify_otp(request):
    try:
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        # Validate email format (you can reuse your validation logic here if needed)
        if not email or not isinstance(email, str) or '@' not in email or '.' not in email:
            raise ValidationError("Invalid email format")

        # Basic email domain validation (customize as needed)
        if not email.endswith('@gmail.com'):
            raise ValidationError("Invalid email domain")

        # Fetch OTP from database for the provided email
        otp_instance = OTP.objects.filter(email=email).order_by('-timestamp').first()

        if not otp_instance:
            raise ValidationError("OTP not found for this email")

        expected_otp = otp_instance.otp

        # Compare entered OTP with expected OTP
        if otp_entered == expected_otp:
            # Optionally, delete the OTP instance after successful verification
            otp_instance.delete()
            return JsonResponse({'message': 'OTP verified successfully'})
        else:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        error_message = f'An error occurred while verifying OTP: {str(e)}'
        return JsonResponse({'error': error_message}, status=500)