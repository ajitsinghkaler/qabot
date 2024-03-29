"""
URL configuration for qa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from qabot.api import DocumentViewSet, ChatViewSet, csrf, ping

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"document", DocumentViewSet)
# router.register(r"user", UserViewSet)
router.register(r"chat_messages", ChatViewSet)

urlpatterns = [
    path("api/csrf", csrf, name="csrf"),
    path("api/ping", ping, name="ping"),
    path("api/", include(router.urls)),
    path("admin", admin.site.urls),
]
