"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from app import views
import app.admin

urlpatterns = [
    path('', views.index),
    path('app/admin/', app.admin.admin.site.urls),
    path('login/', views.login),
    path('login/api/', views.login_api),
    path('register/api/user/', views.register_api_user),
    path('register/', views.register),
    path('register/api/teacher/', views.register_api_teacher),
    path('register/api/admin/', views.register_api_admin),
]
