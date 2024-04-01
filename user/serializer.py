from rest_framework import serializers
from . import models


class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def get_avatar(self, obj):
        avatar = obj.avatar.first()
        if avatar is None:
            return None
        return avatar.avatar.url


