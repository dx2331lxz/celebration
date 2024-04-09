from django.db import models
# 导入django自带的用户模型


# Create your models here.
class UserInfo(models.Model):
    REQUIRED_FIELDS = ['roles']
    USERNAME_FIELD = 'openid'
    username = models.CharField(max_length=32, verbose_name='用户名', blank=True, null=True)
    password = models.CharField(max_length=64, null=True, blank=True)
    openid = models.CharField(max_length=64, null=True, blank=True,unique=True)
    session_key = models.CharField(verbose_name='微信session_key', max_length=400, null=True, blank=True)
    roles_choices = [
        (1, '普通用户'),
        (2, '管理员'),
    ]
    roles = models.IntegerField(choices=roles_choices, default=1)
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name='自我介绍')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='电话号码')
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    # 认证状态
    authentication_status_choices = [
        (1, '未认证'),
        (2, '认证中'),
        (3, '已认证'),
    ]
    authentication_status = models.IntegerField(choices=authentication_status_choices, default=1)




    def __str__(self):
        return self.username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def is_active(self):
        return True


class Avatar(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='avatar')
    avatar = models.ImageField(upload_to='avatar', verbose_name='头像')
    avatar_name = models.CharField(max_length=100, verbose_name='头像名称')

    def __str__(self):
        return self.avatar.url




