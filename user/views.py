from django.shortcuts import render, HttpResponse
from . import serializer, models
from authentication.models import Student, Teacher
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination  # 状态和分页
import json
import os
from celebration import settings
from .models import UserInfo
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
# Create your views here.
# 认证后台
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import requests
from django.contrib import admin
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes




class MyCustomBackend(ModelBackend):
    def authenticate(self, request, openid=None, password=None, **kwargs):
        try:
            user = models.UserInfo.objects.get(openid=openid)
            if user.password == password:
                return user
        except Exception as e:
            return None


def get_login_info(code):
    code_url = settings.code2Session.format(settings.AppId, settings.AppSecret, code)

    response = requests.get(code_url)
    json_response = response.json()  # 把它变成json的字典
    if json_response.get("session_key"):
        return json_response
    else:
        return False


# 微信登录（没有账号就注册）
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        param = request.data
        if not param.get('code'):
            return Response({'code': 403, "msg": "缺少参数"}, status=status.HTTP_403_FORBIDDEN)
        else:
            code = param.get('code')
            user_data = get_login_info(code)
            try:
                if user_data:
                    openid = user_data['openid']
                    session_key = user_data['session_key']

                    user, created = UserInfo.objects.update_or_create(
                        openid=openid,
                        defaults={'session_key': session_key})
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)
                    return Response({'access_token': access_token, 'refresh_token': refresh_token})
                else:
                    return Response({'code': 403, 'msg': "无效的code"})
            except UserInfo.DoesNotExist:
                return Response({'code': 403, 'msg': '查询失败'}, status=status.HTTP_403_FORBIDDEN)


# 修改个人信息

## 获取所有个人信息

class InfoAPIView(APIView):
    def get(self, request):
        id = request.user.id
        user = UserInfo.objects.get(id=id)
        serializers = serializer.AvatarSerializer(instance=user)
        return Response(serializers.data)


## 修改头像

class AvatarAPIView(APIView):
    def post(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        avatar = request.FILES.get('avatar')
        if not avatar:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if models.Avatar.objects.filter(user=user):
                self.delete(request)
            avatar_name = avatar.name
            models.Avatar.objects.create(user=user, avatar=avatar, avatar_name=avatar_name)
            return Response({'code': 200, 'msg': '上传成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        try:
            avatar = models.Avatar.objects.get(user=user)
            return Response({'avatar': avatar.avatar.url})
        except models.Avatar.DoesNotExist:
            return Response({'avatar': None})

    def delete(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        try:
            avatar = models.Avatar.objects.get(user=user)
            path = avatar.avatar.path
            os.remove(path)
            avatar.delete()
            return Response({'code': 200, 'msg': '删除成功'}, status=status.HTTP_200_OK)
        except models.Avatar.DoesNotExist:
            return Response({'code': 403, 'msg': '删除失败'}, status=status.HTTP_403_FORBIDDEN)


## 修改昵称
class NicknameAPIView(APIView):
    def post(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        nickname = request.data.get('nickname')
        if not nickname:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        else:
            user.username = nickname
            user.save()
            return Response({'code': 200, 'msg': '修改成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        return Response({'nickname': user.username}, status=status.HTTP_200_OK)


## 修改手机号
class PhoneAPIView(APIView):
    def post(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        phone = request.data.get('phone')
        if not phone:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        else:
            user.phone = phone
            user.save()
            return Response({'code': 200, 'msg': '修改成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        return Response({'phone': user.phone}, status=status.HTTP_200_OK)


## 修改邮箱


class EmailAPIView(APIView):
    def post(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        email = request.data.get('email')
        if not email:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        else:
            user.email = email
            user.save()
            return Response({'code': 200, 'msg': '修改成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        return Response({'email': user.email}, status=status.HTTP_200_OK)


## 自我介绍
class DescriptionAPIView(APIView):
    def post(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        description = request.data.get('description')
        user.description = description
        user.save()
        return Response({'code': 200, 'msg': '修改成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        return Response({'description': user.description}, status=status.HTTP_200_OK)

# 微信号
class WechatAPIView(APIView):
    def post(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        wechat = request.data.get('wechat')
        user.wechat = wechat
        user.save()
        return Response({'code': 200, 'msg': '修改成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        return Response({'wechat': user.wechat}, status=status.HTTP_200_OK)

# QQ号
class QQAPIView(APIView):
    def post(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        qq = request.data.get('qq')
        user.qq = qq
        user.save()
        return Response({'code': 200, 'msg': '修改成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        id = request.user.id
        user = models.UserInfo.objects.get(id=id)
        return Response({'qq': user.qq}, status=status.HTTP_200_OK)















# 获取自身认证信息

class AuthenticationInfoAPIView(APIView):
    def get(self, request):
        id = request.user.id
        if Student.objects.filter(user_id=id).exists():
            serializers = serializer.StudentSerializer(instance=models.Student.objects.get(user_id=id))
            return Response(serializers.data)
        elif Teacher.objects.filter(user_id=id).exists():
            serializers = serializer.TeacherSerializer(instance=models.Teacher.objects.get(user_id=id))
            return Response(serializers.data)




