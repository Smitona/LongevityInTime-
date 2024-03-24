from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

app_name = 'users'

router.register('users', VeiwSet)

# Для удаления, изменения и получения(me?)

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
