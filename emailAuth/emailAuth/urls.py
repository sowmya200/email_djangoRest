from django.urls import path, include
from django.contrib import admin
from app.views import send_otp, verify_otp

urlpatterns = [
    path('api/send-otp/', send_otp, name='send_otp'),
    path('api/verify-otp/', verify_otp, name='verify_otp'),
    path('admin/', admin.site.urls),
    # Other URL patterns...
]
