# models.py

from django.db import models

class OTP(models.Model):
    email = models.EmailField(default='example@gmail.com')  # Provide a default email address
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email}"
