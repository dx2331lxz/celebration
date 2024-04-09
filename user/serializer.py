from rest_framework import serializers
from . import models
from authentication.models import Student, Teacher

class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def get_avatar(self, obj):
        avatar = obj.avatar.first()
        if avatar is None:
            return None
        return avatar.avatar.url

    def get_name(self, obj):
        student = Student.objects.filter(user=obj).first()
        teacher = Teacher.objects.filter(user=obj).first()
        if student:
            return student.name
        if teacher:
            return teacher.name
        return None


#     修改返回值
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('openid')
        ret.pop('session_key')
        ret.pop('password')
        return ret


