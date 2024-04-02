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
        if user:
            send_otp_email.delay(email)
            return redirect(reverse('users:otp'))


class OTPView(View):
    def get(self, request):

        return render(
            request, 'otp.html',
        )

    def post(self, request):
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        totp = pyotp.TOTP(pyotp.random_base32(), interval=180)
        if totp.verify(otp):
            user = get_object_or_404(CustomUser, email=email)
            login(request, user)

        return HttpResponse('OTP is verified!')
