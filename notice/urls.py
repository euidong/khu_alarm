from . import views
from django.urls import path


urlpatterns =[
    path('total', views.noticeList.as_view()),
    path('my', views.myNoticeList.as_view()),
    path('api/', views.noticeListApi.as_view()),
]