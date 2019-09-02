from django.contrib.auth.models import User
from django.db import models

class myUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    using_klas = models.BooleanField(default=False)
    klas_id = models.CharField(max_length=100, default='0')
    klas_pw = models.CharField(max_length=100, default='0')
    class_id_1 = models.IntegerField(default='0')
    class_id_2 = models.IntegerField(default='0')
    class_id_3 = models.IntegerField(default='0')
    class_id_4 = models.IntegerField(default='0')
    class_id_5 = models.IntegerField(default='0')
    class_id_6 = models.IntegerField(default='0')
    class_id_7 = models.IntegerField(default='0')
    class_id_8 = models.IntegerField(default='0')
    class_id_9 = models.IntegerField(default='0')
    class_id_10 = models.IntegerField(default='0')
    class Meta:
        db_table = 'myUser'