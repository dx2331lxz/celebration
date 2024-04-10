from rest_framework import serializers
from . import models


class BlessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bless
        fields = "__all__"


class DiscussSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    # 评论数量
    comment_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = models.Discuss
        fields = "__all__"

    def get_image(self, obj):
        image = obj.image.all()
        return ImageSerializer(instance=image, many=True).data

    def get_avatar(self, obj):
        avatar = obj.user.avatar.first()
        if avatar is None:
            return None
        return avatar.avatar.url

    def get_username(self, obj):
        return obj.user.username

    def get_comment_count(self, obj):
        return obj.comment.all().count()

    def get_is_like(self, obj):

        userid = self.context['request'].user.id
        if models.Like.objects.filter(user_id=userid, discuss_id=obj.id).exists():
            return True
        return False


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = "__all__"

    def get_avatar(self, obj):
        avatar = obj.user.avatar.first()

        if avatar is None:
            return None
        return avatar.avatar.url

    def get_username(self, obj):
        return obj.user.username


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = "__all__"
