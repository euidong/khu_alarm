from . import views
from django.urls import path


urlpatterns =[
    path('on/', views.pushing),
    path('off/', views.offPushing),
]
