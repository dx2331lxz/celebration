from rest_framework import serializers
from . import models


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Map
        fields = "__all__"

    # 修改返回的字段
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = ""
        data['value'] = [data['lon'], data['lat'], data['value']]
        data.pop('lon')
        data.pop('lat')
        data.pop('id')
        data.pop('nation')
        return data
