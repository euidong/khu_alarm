from django.db import models

# Create your models here.

class Homework (models.Model) :
    name = models.CharField(max_length=100)
    date = models.DateField()
    class Meta:
        db_table = 'homework'

class Class (models.Model) :
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'class'

class Push (models.Model) :
    user_id = models.IntegerField()
    token = models.CharField(max_length=100)
    enable_push = models.BooleanField()
    class Meta:
        db_table = 'push'


