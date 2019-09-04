from .models import Khu_ce_notice, Khu_sw_notice, Personal_notice
from .serializers import Ce_noticeSerializer, Sw_noticeSerializer, Personal_noticeSerializer
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
            sw_notice = Khu_sw_notice.objects.all()
            context ={'ce_notice': ce_notice, 'sw_notice': sw_notice}
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
                            Personal_notice.objects.get(userId_id=request.user.id, noticeId=key[2:])
                        except ObjectDoesNotExist:
                            personal_notice =Personal_notice(userId_id=request.user.id, siteId=0, noticeId=key[2:])
                            personal_notice.save()
                        return redirect('./total')
                    elif key[:2] == 'sw':
                        try :
                            Personal_notice.objects.get(userId_id=request.user.id, noticeId=key[2:])
                        except ObjectDoesNotExist:
                            personal_notice =Personal_notice(userId_id=request.user.id, siteId=1, noticeId=key[2:])
                            personal_notice.save()
                        return redirect('./total')
            return redirect('/')

class ceNoticeListApi(APIView):
    def get(self, request, format=None):
        ce_notice = Khu_ce_notice.objects.all()
        serializer = Ce_noticeSerializer(ce_notice, many=True)
        return Response(serializer.data)

class swNoticeListApi(APIView):
    def get(self, request, format=None):
        sw_notice = Khu_sw_notice.objects.all()
        serializer = Sw_noticeSerializer(sw_notice, many=True)
        return Response(serializer.data)

class myNoticeList(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            personal_notice = Personal_notice.objects.filter(userId_id=request.user.id)
            result_notice = []
            for checker in personal_notice :
                try:
                    if checker.siteId == 0:
                        result_notice.append(Khu_ce_notice.objects.get(id=checker.noticeId))
                    elif checker.siteId == 1:
                        result_notice.append(Khu_sw_notice.objects.get(id=checker.noticeId))
                except ObjectDoesNotExist: # 해당 자료가 삭제되었을 경우 개인목록에서도 삭제한다.
                    checker.delete()
            context ={'result_notice': result_notice}
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
                    delete_notice =Personal_notice.objects.get(userId_id=request.user.id, noticeId = key)
                    delete_notice.delete()
                    return redirect('./my')
            return redirect('/')
            