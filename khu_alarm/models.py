from django.contrib.auth.models import User
from django.db import models

class myUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    using_klas = models.BooleanField(default=False)
    klas_id = models.CharField(max_length=100, default='0')
    klas_pw = models.CharField(max_length=100, default='0')
    class Meta:
        db_table = 'myUser'
