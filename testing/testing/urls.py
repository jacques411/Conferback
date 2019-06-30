"""testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import django.contrib.admindocs.urls

from django.contrib import admin
from django.urls import path, include, re_path

from Conferauth.views import CuserView, profile_view, login, example_view, logout, create_user

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views


router = DefaultRouter()
router.register(r'users', CuserView)
#router.register(r'groups', GroupView)
#router.register(r'sheets', SheetView)
#router.register(r'annonces', AnnonceView)
#router.register(r'template', TemplateView)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),
    path('ex/', example_view, name='example_view'),
    path('create_user/', create_user, name='create_user'),
    path('admin/docs/', include('django.contrib.admindocs.urls')),
]
