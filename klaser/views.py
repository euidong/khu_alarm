from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Push
from .serializers import PushSerializer
# Create your views here.

@api_view(['POST'])
def pushing(request) :
    if request.method == 'POST':
        serializer = PushSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def offPushing(request) :
    push = Push.objects.get(username=request.data['username'])
    push.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
