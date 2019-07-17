from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Khu_ce_notice (models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    url = models.URLField()

    class Meta:
        db_table = 'khu_ce_notice'
        ordering = ['-id']

class Khu_sw_notice (models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    url = models.URLField()

    class Meta:
        db_table = 'khu_sw_notice'
        ordering = ['-id']

class Personal_notice(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    siteId = models.SmallIntegerField()
    noticeId = models.SmallIntegerField()

    class Meta:
        db_table = 'personal_notice'

