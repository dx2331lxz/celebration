from django.shortcuts import render, HttpResponse
from . import serializer, models
from user.models import UserInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination  # 状态和分页
from rest_framework.parsers import MultiPartParser  # 文件上传`MultiPartParser`解析器
import json
import os
from utils.sendemail import send_email

# 学生认证

class StudentAuthenticatedAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        id = request.user.id
        serializers = serializer.StudentSerializer(instance=models.Student.objects.get(user_id=id))
        return Response(serializers.data)

    def post(self, request):
        id = request.user.id
        user = UserInfo.objects.get(id=id)
        # send_email('学生')
        if user.authentication_status != 1:
            return Response({'msg': '请等待回复，不要重复操作'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['user'] = id
        serializers = serializer.StudentSerializer(data=request.data)
        if serializers.is_valid():

            serializers.save()

            user.authentication_status = 2
            user.save()
            send_email('学生')
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# todo 教师认证
class TeacherAuthenticatedAPIView(APIView):
    parser_classes = [MultiPartParser]

    def get(self, request):
        id = request.user.id
        serializers = serializer.TeacherSerializer(instance=models.Teacher.objects.get(user_id=id))
        return Response(serializers.data)

    def post(self, request):
        id = request.user.id

        user = UserInfo.objects.get(id=id)
        if user.authentication_status != 1:
            return Response({'msg': '请等待回复，不要重复操作'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['user'] = id
        serializers = serializer.TeacherSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            user.authentication_status = 2
            user.save()
            send_email('教师')
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# 审核认证

class AuthenticationAPIView(APIView):
    def get(self, request):
        user = UserInfo.objects.get(id=request.user.id)
        if user.roles != 2:
            return Response({'msg': '无权限'}, status=status.HTTP_400_BAD_REQUEST)
        students = models.Student.objects.filter(user__authentication_status=2)
        teachers = models.Teacher.objects.filter(user__authentication_status=2)
        students_serializers = serializer.StudentSerializer(students, many=True)
        teachers_serializers = serializer.TeacherSerializer(teachers, many=True)
        serializers = {
            'students': students_serializers.data,
            'teachers': teachers_serializers.data
        }

        return Response(serializers)

    def post(self, request):
        if UserInfo.objects.get(id=request.user.id).roles != 2:
            return Response({'msg': '无权限'})
        data = request.data
        form_id = data.get('form_id')
        form_type = data.get('form_type')
        id = data.get('id')
        status = int(data.get('status'))

        if form_type == "student":
            if models.Student.objects.filter(id=form_id).count() == 0:
                return Response({'msg': '表单不存在'})


        if form_type == "teacher":
            if models.Teacher.objects.filter(id=form_id).count() == 0:
                return Response({'msg': '表单不存在'})

        user = UserInfo.objects.get(id=id)

        user.authentication_status = status
        if status == 1:
            if form_type == "student":
                student = models.Student.objects.get(user_id=user.id)
                path = student.Diploma.path
                if os.path.exists(path):
                    os.remove(path)
                path = student.Degree_certificate.path
                if os.path.exists(path):
                    os.remove(path)
                student.delete()
            if form_type == "teacher":
                teacher = models.Teacher.objects.get(user_id=user.id)
                path = teacher.work_certificate.path
                if os.path.exists(path):
                    os.remove(path)
                teacher.delete()

        user.save()
        return Response({'msg': '操作成功'})


# 添加专业
class ProfessionalAPIView(APIView):
    def post(self, request):
        data = request.data

        serializers = serializer.ProfessionalSerializer(data=data, many=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
