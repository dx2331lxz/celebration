from django.shortcuts import render, HttpResponse
from . import serializer, models
from user.models import UserInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination  # 状态和分页
from rest_framework.parsers import MultiPartParser, JSONParser # 文件上传`MultiPartParser`解析器
import json
import os


# 上传祝福
class BlessAPIView(APIView):
    def post(self, request):
        userid = request.user.id
        content = request.data.get('content')
        if not content:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        models.Bless.objects.update_or_create(user_id=userid, defaults={'content': content})
        return Response({'msg': '上传成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        bless = models.Bless.objects.all()
        serializers = serializer.BlessSerializer(bless, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.data.get('id')
        userid = request.user.id
        user = UserInfo.objects.get(id=userid)
        # 验证权限
        if user.roles != 2:
            return Response({'msg': '权限不足'}, status=status.HTTP_403_FORBIDDEN)
        try:
            bless = models.Bless.objects.get(user_id=id)
            bless.delete()
            return Response({'msg': '删除成功'}, status=status.HTTP_200_OK)
        except models.Bless.DoesNotExist:
            return Response({'msg': '不存在'}, status=status.HTTP_404_NOT_FOUND)


# 上传图片(只用了上传图片，并且返回图片路径)
class ImageAPIView(APIView):
    parser_classes = [MultiPartParser, JSONParser]

    # 上传单张图片
    def post(self, request):
        photo = request.FILES.get('photo')
        if not photo:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        image = models.Image.objects.create(image=photo)
        serializers = serializer.ImageSerializer(image)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.data.get('id')
        try:
            image = models.Image.objects.get(id=id)
            path = image.image.path
            os.remove(path)
            image.delete()
            return Response({'msg': '删除成功'}, status=status.HTTP_200_OK)
        except models.Image.DoesNotExist:
            return Response({'msg': '不存在'}, status=status.HTTP_404_NOT_FOUND)


class DiscussAPIView(APIView):
    def post(self, request):
        userid = request.user.id
        user = UserInfo.objects.get(id=userid)
        param = request.data
        content = param.get('content')
        photos = param.get('photos').split(',')
        discuss = models.Discuss.objects.create(user=user, content=content)
        for id in photos:
            id = int(id)
            models.Image.objects.update_or_create(id=id, defaults={'discuss': discuss})

        return Response({'msg': '上传成功'}, status=status.HTTP_200_OK)

    def get(self, request):
        discuss = models.Discuss.objects.all().order_by('-create_time')
        serializers = serializer.DiscussSerializer(discuss, many=True, context={'request': request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.data.get('id')
        userid = request.user.id
        user = UserInfo.objects.get(id=userid)
        # 验证权限
        if user.roles != 2:
            return Response({'msg': '权限不足'}, status=status.HTTP_403_FORBIDDEN)
        try:
            discuss = models.Discuss.objects.get(id=id)
            images = models.Image.objects.filter(discuss=discuss)
            for image in images:
                path = image.image.path
                os.remove(path)
                image.delete()
            discuss.delete()
            return Response({'msg': '删除成功'}, status=status.HTTP_200_OK)
        except models.Discuss.DoesNotExist:
            return Response({'msg': '不存在'}, status=status.HTTP_404_NOT_FOUND)


# 评论
class CommentAPIView(APIView):
    def post(self, request):
        userid = request.user.id
        user = UserInfo.objects.get(id=userid)
        param = request.data
        discuss_id = param.get('discuss_id')
        content = param.get('content')
        try:
            discuss = models.Discuss.objects.get(id=discuss_id)
            models.Comment.objects.create(user=user, discuss=discuss, content=content)
            return Response({'msg': '评论成功'}, status=status.HTTP_200_OK)
        except models.Discuss.DoesNotExist:
            return Response({'msg': '讨论不存在'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        id = request.query_params.get('discuss_id')
        comment = models.Comment.objects.filter(discuss_id=id)
        serializers = serializer.CommentSerializer(comment, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.data.get('id')
        userid = request.user.id
        user = UserInfo.objects.get(id=userid)
        # 验证权限
        if user.roles != 2:
            return Response({'msg': '权限不足'}, status=status.HTTP_403_FORBIDDEN)
        try:
            comment = models.Comment.objects.get(id=id)
            comment.delete()
            return Response({'msg': '删除成功'}, status=status.HTTP_200_OK)
        except models.Comment.DoesNotExist:
            return Response({'msg': '不存在'}, status=status.HTTP_404_NOT_FOUND)


# 点赞
class LikeAPIView(APIView):
    def post(self, request):
        data = request.data
        discuss_id = data.get('id')
        if not discuss_id:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        if models.Like.objects.filter(user_id=request.user.id, discuss_id=discuss_id).exists():
            return Response({'msg': '已点赞'}, status=status.HTTP_200_OK)
        try:
            discuss = models.Discuss.objects.get(id=discuss_id)
            discuss.like += 1
            models.Like.objects.create(user_id=request.user.id, discuss_id=discuss_id)
            discuss.save()
            return Response({'msg': '点赞成功'}, status=status.HTTP_200_OK)
        except models.Discuss.DoesNotExist:
            return Response({'msg': '讨论不存在'}, status=status.HTTP_404_NOT_FOUND)

    # 取消点赞
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        if not models.Like.objects.filter(user_id=request.user.id, discuss_id=id).exists():
            return Response({'msg': '未点赞'}, status=status.HTTP_200_OK)
        try:
            discuss = models.Discuss.objects.get(id=id)
            if discuss.like == 0:
                return Response({'msg': '未点赞'}, status=status.HTTP_200_OK)
            discuss.like -= 1
            models.Like.objects.filter(user_id=request.user.id, discuss_id=id).delete()
            discuss.save()
            return Response({'msg': '取消点赞成功'}, status=status.HTTP_200_OK)
        except models.Discuss.DoesNotExist:
            return Response({'msg': '讨论不存在'}, status=status.HTTP_404_NOT_FOUND)
