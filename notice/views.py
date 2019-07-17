from .models import Khu_ce_notice, Personal_notice
from .serializers import Ce_noticeSerializer, Personal_noticeSerializer
from django.shortcuts import render, redirect
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class noticeList(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            ce_notice = Khu_ce_notice.objects.all()
            context ={'context': ce_notice}
            return render(request, 'notice.html', context)
        else :
            return redirect('/')
        # logout
    def post(self, request, format=None): 
        if 'logout' in request.data:
            logout(request)
            return redirect('/')
        else:
            for key in request.data:
                if key != 'csrfmiddlewaretoken':
                    if key[:2] == 'ce':
                        try :
                            Personal_notice.objects.get(userId_id= request.user.id, noticeId=key[2:])
                        except ObjectDoesNotExist:
                            personal_notice =Personal_notice(userId_id=request.user.id, siteId=0, noticeId=key[2:])
                            personal_notice.save()
                        return redirect('./total')
            return redirect('/')

class noticeListApi(APIView):
    def get(self, request, format=None):
        ce_notice = Khu_ce_notice.objects.all()
        serializer = Ce_noticeSerializer(ce_notice, many=True)
        return Response(serializer.data)

class myNoticeList(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            personal_notice = Personal_notice.objects.filter(userId_id=request.user.id)
            result_notice = []
            for checker in personal_notice :
                result_notice.append(Khu_ce_notice.objects.get(id=checker.noticeId))
            context ={'context': result_notice}
            return render(request, 'my_notice.html', context)
        else :
            return redirect('/')
    def post(self, request, format=None):
        if 'logout' in request.data:
            logout(request)
            return redirect('/')
        else:
            for key in request.data:
                if key != 'csrfmiddlewaretoken':
                    if key[:2] == 'ce':
                        delete_notice =Personal_notice.objects.get(userId_id=request.user.id, noticeId = key[2:])
                        delete_notice.delete()
                        return redirect('./my')
            return redirect('/')
            