from django.db import models


# Create your models here.


class Bless(models.Model):
    user = models.ForeignKey('user.UserInfo', on_delete=models.CASCADE, related_name='bless')
    content = models.TextField(verbose_name='content')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create time')

    def __str__(self):
        return self.user.username


# 评论
class Discuss(models.Model):
    user = models.ForeignKey('user.UserInfo', on_delete=models.CASCADE, related_name='discuss')
    content = models.TextField(verbose_name='content')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create time')
    like = models.IntegerField(default=0, verbose_name='like')

    def __str__(self):
        return self.user.username

# 讨论的图片
class Image(models.Model):
    discuss = models.ForeignKey('Discuss', on_delete=models.CASCADE, related_name='image', null=True, blank=True)
    image = models.ImageField(upload_to='discuss', verbose_name='image')

    def __str__(self):
        return self.discuss.user.username

# 评论
class Comment(models.Model):
    user = models.ForeignKey('user.UserInfo', on_delete=models.CASCADE, related_name='comment')
    discuss = models.ForeignKey('Discuss', on_delete=models.CASCADE, related_name='comment')
    content = models.TextField(verbose_name='content')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='create time')

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey('user.UserInfo', on_delete=models.CASCADE, related_name='like_record')
    discuss = models.ForeignKey('Discuss', on_delete=models.CASCADE, related_name='like_record')

    def __str__(self):
        return self.user.username




