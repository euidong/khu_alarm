from django.contrib.auth.models import User
from .models import myUser
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from rest_framework import generics
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import is_password_usable, make_password

class main(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            context = {'user' : request.user}
            return render(request, 'main.html')
        else:
            return redirect('/sign_in')

    # logout
    def post(self, request, format=None):
        if request.data['logout'] == "logout":
            logout(request)
        return redirect('/')

class signIn(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            raise PermissionDenied
        context = {'message':'hello'}
        return render(request, 'sign_in.html', context)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            raise PermissionDenied
        users = User.objects.all()
        for user in users:
            if request.data['email'] == user.email:
                if user.check_password(request.data['password']):
                    login(request, user)
                    return redirect('/')
                else :
                    context ={'message' : 'password is wrong'}
                    return render(request, 'sign_in.html', context)
        context = {'message': 'email is not exist!!'}
        return render(request, 'sign_in.html', context)

# 로그인 되어있으면 못들어오게 데코레이터 만들어보자
class signUp(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            raise PermissionDenied
        return render(request, 'sign_up.html')
    def post(self, request, format=None):
        if request.user.is_authenticated:
            raise PermissionDenied
        users = User.objects.all()
        for user in users:
            if user.email == request.data['email']:
                return render(request, 'sign_up.html', {'message':'already existed email.'})
            if user.username == request.data['username']:
                return render(request, 'sign_up.html', {'message':'already existed username.'})
        if is_password_usable(request.data['password']) and request.data['first_name'] != '' and request.data['last_name'] != '':
            user = User.objects.create_user(username= request.data['username'],email= request.data['email']) 
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.set_password(request.data['password'])
            user.save()
            myuser = myUser.objects.create(user_id=user.id)
            return redirect('/sign_in')
        else:
            return render(request, 'sign_up.html', {'message': 'wrong input.'})



# my page 할때 사용합시다.(put만 만들어놓음.) user 정보 return
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk): # 객체 생성
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None): # 확인
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None): # 수정
        user = self.get_object(pk)
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None): # 삭제
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  





# signIn api
class signInApi(APIView):
    def post(self, request):
        users = User.objects.all()
        for user in users:
            if request.data['email'] == user.email:
                if user.check_password(request.data['password']):
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                else :
                    return JsonResponse({"error" : 'password is wrong'})
        return JsonResponse({"error" : 'email is not exist'})


class signUpApi(APIView):
    def post(self,request):
        users = User.objects.all()
        for user in users:
            if user.email == request.data['email']:
                return Response({"error":"already existed email."},status=status.HTTP_400_BAD_REQUEST)
            if user.username == request.data['username']:
                return Response({"error":"already existed username."},status=status.HTTP_400_BAD_REQUEST)
        if is_password_usable(request.data['password']) and request.data['first_name'] != '' and request.data['last_name'] != '':
            user = User.objects.create_user(username= request.data['username'],email= request.data['email']) 
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.set_password(request.data['password'])
            user.save()
            myuser = myUser.objects.create(user_id=user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "wrong input."}, status=status.HTTP_400_BAD_REQUEST)

class signOutApi(APIView):
    def post(self,request):
        user = User.objects.get(username=request.data['username'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class getKlasData(APIView):
    def post(self,request):
        default_user = User.objects.get(username=request.data['username'])
        user = myUser.objects.get(user_id=default_user.id)
        user.using_klas = True
        user.klas_id = request.data['klas_id']
        user.klas_pw = request.data['klas_pw']
        user.save()
        return Response(status=status.HTTP_200_OK) 
