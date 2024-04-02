import datetime as dt
import pyotp

from django.core.mail import send_mail

from longevity_backend import settings
from celery import shared_task


@shared_task()
def send_otp_email(user_email):

    send_mail(
        'OTP',
        f'Your OTP code is {generate_otp()}',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=180)
    otp = totp.now()

    return otp
