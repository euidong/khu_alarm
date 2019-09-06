from .models import Push
from rest_framework import serializers

class PushSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Push
        fields = ('token','username','enable_push')

