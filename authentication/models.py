from django.db import models


# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(to='user.UserInfo', to_field='id', related_name='student', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='姓名')
    degree_options = (
        ('1', '专科生'),
        ('2', '本科生'),
        ('3', '联培本科'),
        ('4', '硕士研究生'),
        ('5', '联培硕士'),
        ('6', '博士研究生'),
        ('7', '联培博士'),
        ('8', '博士后'),
        ('9', '继续教育和培训'),
    )
    degree = models.CharField(max_length=2, choices=degree_options, verbose_name='学位')
    status_options = (
        ('1', '在读'),
        ('2', '毕业'),
    )
    status = models.CharField(max_length=2, choices=status_options, verbose_name='学籍状态')
    start_time = models.DateField(verbose_name='入学时间')
    end_time = models.DateField(verbose_name='毕业时间', null=True, blank=True)
    # 图片
    Diploma = models.ImageField(verbose_name='学历证书', upload_to='student/', null=True, blank=True)
    # 学位证书
    Degree_certificate = models.ImageField(verbose_name='学位证书', upload_to='student/', null=True, blank=True)

    professional = models.CharField(max_length=100, verbose_name='专业名称')


class Teacher(models.Model):
    user = models.OneToOneField(to='user.UserInfo', to_field='id', related_name='teacher', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='姓名')
    status_options = (
        ('1', '在职'),
        ('2', '已离职'),
    )

    status = models.CharField(max_length=2, choices=status_options, verbose_name='在职状态')

    #     在校时间
    start_time = models.DateField(verbose_name='入职时间')

    end_time = models.DateField(verbose_name='离职时间', null=True, blank=True)
    #     部门或实验室名称
    department = models.CharField(max_length=100, verbose_name='部门名称')
    #     备注
    remark = models.TextField(verbose_name='备注', null=True, blank=True)
    #     工作证
    work_certificate = models.ImageField(verbose_name='工作证', upload_to='teacher/')


class Professional(models.Model):
    name = models.CharField(max_length=100, verbose_name='专业名称', unique=True)


# 培养单位
class TrainingUnit(models.Model):
    student = models.ForeignKey(to='Student', to_field='id', related_name='training_unit', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='培养单位名称')

