"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('login/oauth2/', views.discord_login, name='oauth2_login'),
    path('login/oauth2/redirect', views.discord_login_redirect, name='discord_login_redirect'),
    path('register/',views.register, name='register'),
    path('disconnect/', views.disconnect_discord, name='disconnect'),
    path('timezone/', views.select_timezone, name='timezone'),
    path('verify/', views.admin_verify, name='admin_verify'),
    path('purchase/',views.my_purchase, name='my_purchase'),
    path('result/', views.result, name='topup'),
    path('transactions/', views.trans, name='trans'),
    path('mybot/', views.mybot, name='mybot'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)