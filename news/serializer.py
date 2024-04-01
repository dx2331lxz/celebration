from rest_framework import serializers
from . import models

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = ["title", "created_at", "updated_at", "published", "image", "id"]


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = "__all__"


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('content')
        return data


    def get_photos(self, obj):
        photos = obj.photo.all()
        return PhotoSerializer(instance=photos, many=True).data

class ActivityDetailSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = "__all__"

    def get_photos(self, obj):
        photos = obj.photo.all()
        return PhotoSerializer(instance=photos, many=True).data


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Photo
        fields = "__all__"