from .models import Push
from rest_framework import serializers

class PushSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Push
        fields = ('user_id', 'token', 'enable_push')

