from . import views
from django.urls import path


urlpatterns =[
    path('total', views.noticeList.as_view()),
    path('my', views.myNoticeList.as_view()),
    path('ce_api/', views.ceNoticeListApi.as_view()),
    path('sw_api/', views.swNoticeListApi.as_view()),
]