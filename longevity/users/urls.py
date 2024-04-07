from django.urls import include, path

from rest_framework.routers import SimpleRouter

from users.views import CustomUserViewSet, LoginView, OTPView

router = SimpleRouter()

app_name = 'users'

router.register(
    r'user/(?P<user_id>\d+)',
    CustomUserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('otp/', OTPView.as_view(), name='otp'),
]
