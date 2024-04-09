from django.db import models

# Create your models here.
class Map(models.Model):
    name = models.CharField(max_length=32, verbose_name='city')
    nation = models.CharField(max_length=32, verbose_name='nation')
    lon = models.FloatField(verbose_name='longitude')
    lat = models.FloatField(verbose_name='latitude')
    value = models.IntegerField(default=10, verbose_name='value')
    def __str__(self):
        return self.province


# 记录已经点亮过的用户
class UserMap(models.Model):
    user = models.ForeignKey('user.UserInfo', on_delete=models.CASCADE, related_name='usermap')
    map = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='usermap')
    def __str__(self):
        return self.user.username