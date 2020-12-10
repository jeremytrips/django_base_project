"""Didit URL Configuration

The `urlpatterns` list routes URLs to classview. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function classview
    1. Add an import:  from my_app import classview
    2. Add a URL to urlpatterns:  path('', classview.home, name='home')
Class-based classview
    1. Add an import:  from other_app.classview import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from .views.authentication import LoginVIew, LogoutView
from .views.registrationview import RegistrationView
from .views.deleteacountview import DeleteAccount
from .views.verifytoken import VerifyToken

urlpatterns = [
    path('create/', RegistrationView.as_view(), name='create'),
    path('delete/', DeleteAccount.as_view(), name='delete'),
    path('login/', LoginVIew.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verifytoken/', VerifyToken.as_view(), name='verify_token')
]
