from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import is_password_usable

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
        
        if is_password_usable(request.data['password']) and request.data['first_name'] != '' and request.data['last_name'] != '':
            user = User.objects.create_user(username= request.data['username'],email= request.data['email']) 
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.set_password(request.data['password'])
            user.save() 
            return redirect('/sign_in')
        else:
            return render(request, 'sign_up.html', {'message': 'wrong input.'})



# user 정보 return
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  