import datetime as dt
import pyotp

from django.contrib.auth import authenticate, login
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)

from rest_framework import viewsets
from rest_framework.views import View
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.models import CustomUser
from users.serializers import CustomUserSerializer
from users.tasks import send_otp_email


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    permission_classes = (IsAuthenticatedOrReadOnly,)


class LoginView(View):
    def get(self, request):

        return render(
            request, 'login.html',
        )

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:
            send_otp_email(request, email)
            return redirect(reverse('users:otp')), email
        else:
            return HttpResponse('No such user.')


class OTPView(View):
    def get(self, request):

        return render(
            request, 'otp.html',
        )

    def post(self, request):
        otp = request.POST.get('otp')

        otp_valid_time = request.session['otp_valid_time']
        otp_secret_key = request.session['otp_secret_key']

        valid_time = dt.datetime.fromisoformat(otp_valid_time)

        if dt.datetime.now() < valid_time:

            totp = pyotp.TOTP(otp_secret_key, interval=180)

            if totp.verify(otp):
                email = 
                user = get_object_or_404(CustomUser, email=email)
                login(request, user)

                del request.session['otp_valid_time']
                del request.session['otp_secret_key']

            else:
                return HttpResponse('OTP is not valid!')

        else:
            return HttpResponse('OTP has expired!')

        return HttpResponse('OTP is verified!')
