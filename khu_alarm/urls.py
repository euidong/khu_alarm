"""khu_alarm URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main.as_view()),
    path('user_list/<int:pk>/', views.UserDetail.as_view()),
    path('sign_in/', views.signIn.as_view()),
    path('sign_up/', views.signUp.as_view()),
    path('sign_in_api/', views.signInApi.as_view()),
    path('sign_up_api/', views.signUpApi.as_view()),
    path('sign_out_api/', views.signOutApi.as_view()),
    path('get_klas_data/', views.getKlasData.as_view()),
    path('notice/', include('notice.urls')),
    path('klaser/', include('klaser.urls')),
]
