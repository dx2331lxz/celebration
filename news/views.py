from django.shortcuts import render, HttpResponse
from . import serializer, models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination  # 状态和分页
import json
import os
# import Allowany
from rest_framework.permissions import AllowAny

# Create your views here.

class NewsAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        news = models.News.objects.all()
        ser = serializer.NewSerializer(instance=news, many=True)
        return Response(ser.data)

    def post(self, request):
        param = request.data
        ser = serializer.NewSerializer(data=param)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        news = models.News.objects.get(id=id)
        ser = serializer.NewsDetailSerializer(instance=news)
        return Response(ser.data)

    def put(self, request, id):
        news = models.News.objects.get(id=id)
        param = request.data
        ser = serializer.NewsDetailSerializer(instance=news, data=param)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        news = models.News.objects.get(id=id)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        activity = models.Activity.objects.all()
        ser = serializer.ActivitySerializer(instance=activity, many=True)
        return Response(ser.data)

    def post(self, request):
        param = request.data
        photos = request.FILES.getlist('photos')
        ser = serializer.ActivitySerializer(data=param)
        if ser.is_valid():
            activity = ser.save()
            for photo in photos:
                models.Photo.objects.create(picture=photo, activity=activity)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        activity = models.Activity.objects.get(id=id)
        ser = serializer.ActivityDetailSerializer(instance=activity)
        return Response(ser.data)

    def put(self, request, id):
        try:
            activity = models.Activity.objects.get(id=id)
            param = request.data
            photos = request.FILES.getlist('photos')
            for i in activity.photo.all():
                path = i.picture.path
                os.remove(path)
                i.delete()
            for photo in photos:
                models.Photo.objects.create(picture=photo, activity=activity)
            ser = serializer.ActivityDetailSerializer(instance=activity, data=param)
            if ser.is_valid():
                ser.save()

                return Response(ser.data)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Activity.DoesNotExist:

            return Response({'error': 'activity not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        activity = models.Activity.objects.get(id=id)
        for i in activity.photo.all():
            path = i.picture.path
            os.remove(path)
            i.delete()
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadPhotoAPIView(APIView):

    def post(self, request):
        photos = request.FILES.getlist('photos')
        photo_list = []
        for photo in photos:
            photo_list.append(models.Photo.objects.create(picture=photo))

        return Response({'photos': photo_list}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        param = request.data
        photo_id = param.get('photo_id')
        photo = models.Photo.objects.get(id=photo_id)
        path = photo.picture.path
        os.remove(path)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


