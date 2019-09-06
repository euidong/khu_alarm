from .models import Khu_ce_notice, Khu_sw_notice, Personal_notice
from rest_framework import serializers

class Ce_noticeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Khu_ce_notice
        fields = ('id', 'name', 'date', 'url')

class Sw_noticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Khu_sw_notice
        fields = ('id', 'name', 'date', 'url')

class Personal_noticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personal_notice
        fields = ('userId_id','siteId','noticeId')
