from django.db import models
#

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    published = models.CharField(verbose_name='发布时间', max_length=40, null=True, blank=True)
    image = models.CharField(verbose_name='图片', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 简介
    description = models.TextField(verbose_name='描述')

    def __str__(self):
        return self.title


class Activity(models.Model):
    Author = models.ForeignKey(to='user.UserInfo', to_field='id', related_name='activity', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    description = models.TextField(verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    start_time = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)

    def __str__(self):
        return self.title


class Photo(models.Model):
    news = models.ForeignKey(to_field='id', to=News, related_name='photo', on_delete=models.CASCADE, null=True,
                             blank=True)
    activity = models.ForeignKey(to_field='id', to=Activity, related_name='photo', on_delete=models.CASCADE, null=True,
                                 blank=True)
    picture = models.ImageField(verbose_name="图片", upload_to="message/")

    def __str__(self):
        return self.picture_name
