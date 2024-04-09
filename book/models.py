from django.db import models


# Create your models here.

class Address(models.Model):
    user = models.ForeignKey('user.UserInfo', on_delete=models.CASCADE, related_name='address')
    avatar = models.CharField(max_length=64, verbose_name='头像')
    name = models.CharField(max_length=20, verbose_name='姓名')

    def __str__(self):
        return self.address
