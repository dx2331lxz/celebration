from django.shortcuts import render, HttpResponse
from . import serializer, models
from user.models import Avatar, UserInfo
from authentication.models import Student, Teacher
from user.serializer import AvatarSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination  # 状态和分页
from rest_framework.parsers import MultiPartParser  # 文件上传`MultiPartParser`解析器
import json
import os


class AddressAPIView(APIView):
    def get(self, request):
        userlist = UserInfo.objects.filter(authentication_status=3)
        ret = []

        students = Student.objects.filter(user__in=userlist)
        teachers = Teacher.objects.filter(user__in=userlist)
        if students:
            for student in students:
                user = student.user
                avatar = Avatar.objects.filter(user=user).first()
                if avatar:
                    avatar_url = avatar.avatar.url
                else:
                    avatar_url = ''
                ret.append({
                    'id': user.id,
                    'name': student.name,
                    'avatar': avatar_url,
                })
        if teachers:
            for teacher in teachers:
                user = student.user
                avatar = Avatar.objects.filter(user=user).first()
                if avatar:
                    avatar_url = avatar.avatar.url
                else:
                    avatar_url = ''
                ret.append({
                    'id': user.id,
                    'name': teacher.name,
                    'avatar': avatar_url,
                })

        return Response({"data": ret}, status=status.HTTP_200_OK)


class InfoAPIView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = UserInfo.objects.get(id=id)
            serializers = AvatarSerializer(instance=user)

            return Response(serializers.data)
        except UserInfo.DoesNotExist:
            return Response({'code': 403, 'msg': '查询失败'}, status=status.HTTP_403_FORBIDDEN)
