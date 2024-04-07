import datetime as dt
import pyotp

from django.core.mail import send_mail

from longevity_backend import settings
from celery import shared_task


#@shared_task
def send_otp_email(request, user_email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=180)
    otp = totp.now()

    send_mail(
        'OTP',
        f'Your OTP code is {otp}',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )

    otp_valid_time = dt.datetime.now() + dt.timedelta(minutes=3)
    request.session['otp_valid_time'] = str(otp_valid_time)
    request.session['otp_secret_key'] = totp.secret

    return send_mail
