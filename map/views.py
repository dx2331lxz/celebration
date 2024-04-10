from django.shortcuts import render, HttpResponse

from django.http import JsonResponse
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination  # 状态和分页
import json
import os
from celebration import settings
import requests
from . import serializer
# 导入AllowAny
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import BasePermission

class CustomPermission(BasePermission):
    message = 'You do not have permission to access this resource.'

    def has_permission(self, request, view):
        # 如果请求方法为GET，则允许访问；否则，不允许访问
        if request.method == 'GET':
            return True
        return bool(request.user and request.user.is_authenticated)
#
# from pyecharts import options as opts
# from pyecharts.charts import Geo
# from pyecharts.globals import ChartType, SymbolType


class LightAPIView(APIView):
    permission_classes = [CustomPermission]
    def post(self, request):
        userid = request.user.id
        lon = request.data.get('lon')
        lat = request.data.get('lat')
        if not lon or not lat:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        mapurl = f"http://api.tianditu.gov.cn/geocoder?postStr={{'lon':{lon},'lat':{lat},'ver':1}}&type=geocode&tk={settings.map_apikey}"

        response = requests.get(mapurl)
        information = response.json()

        if information.get('status') != '0':
            return Response({'code': 403, 'msg': '请求失败'}, status=status.HTTP_403_FORBIDDEN)

        city = information.get('result').get('addressComponent').get('city')
        nation = information.get('result').get('addressComponent').get('nation')
        address = information.get('result').get('addressComponent').get('address')
        if not address:
            return Response({'code': 403, 'msg': '无法获取地址'}, status=status.HTTP_403_FORBIDDEN)
        if not city and address:
            city = information.get('result').get('addressComponent').get('address')

        if models.Map.objects.filter(name=city).exists():
            map = models.Map.objects.get(name=city)
            if not models.UserMap.objects.filter(user_id=userid).exists():
                map.value = (map.value + 1) % 50
                if map.value < 10:
                    map.value = 10 + map.value
            map.save()
            models.UserMap.objects.update_or_create(user_id=userid, defaults={'map_id': map.id})
            # serializers = serializer.MapSerializer(map)
            rank = models.UserMap.objects.get(user_id=userid).id
            return Response({'msg': '点亮成功', 'rank': rank}, status=status.HTTP_200_OK)
        cityurl = f"http://api.tianditu.gov.cn/geocoder?ds={{'keyWord':'{city}' }}&tk={settings.map_apikey}"

        response = requests.get(cityurl)
        # print(response.json())
        lon = response.json().get('location').get('lon')
        lat = response.json().get('location').get('lat')

        map = models.Map.objects.create(name=city, lon=lon, lat=lat, nation=nation)
        models.UserMap.objects.update_or_create(user_id=userid, defaults={'map_id': map.id})
        rank = models.UserMap.objects.get(user_id=userid).id
        return Response({'msg': '点亮成功', 'rank': rank}, status=status.HTTP_200_OK)

    def get(self, request):
        maps = models.Map.objects.all()
        serializers = serializer.MapSerializer(maps, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


# 获取地区排名
class RankAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        nations = models.Map.objects.values('nation').distinct()
        data = []
        for nation in nations:
            maps = models.Map.objects.filter(nation=nation.get('nation')).order_by('-value')
            # 将所有map的value加和
            sum = 0
            city = []
            for map in maps:
                city.append({'name': map.name, 'value': map.value})
                sum += map.value
            data.append({'nation': nation.get('nation'), 'value': sum, 'city': city})

        #     将data按照value排序
        data = sorted(data, key=lambda x: x.get('value'), reverse=True)
        return Response(data, status=status.HTTP_200_OK)


# class IndexAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         lon = data.get('lon')
#         lat = data.get('lat')
#         if not lon or not lat:
#             return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
#
#         c = (
#             Geo()
#             .add_schema(
#                 maptype="china",
#                 itemstyle_opts=opts.ItemStyleOpts(color="#ebe7d4", border_color="#dec889"),
#             )
#             .add_coordinate_json()
#             .add(
#                 "",
#                 [("广州", 55), ("北京", 66), ("杭州", 77), ("重庆", 88), ("青岛", 100)],
#                 type_=ChartType.EFFECT_SCATTER,
#                 color="white",
#             )
#             .add(
#                 "geo",
#                 [("广州", "青岛"), ("北京", "青岛"), ("杭州", "青岛"), ("重庆", "青岛")],
#                 type_=ChartType.LINES,
#                 effect_opts=opts.EffectOpts(
#                     symbol=SymbolType.ARROW, symbol_size=6, color="blue"
#                 ),
#                 linestyle_opts=opts.LineStyleOpts(curve=0.2),
#             )
#             .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#
#         )
#         c.render("templates/geo_lines_background.html")
#         return render(request, "geo_lines_background.html")
#
#     def get(self, request):
#         return render(request, "geo_lines_background.html")

class GoHomeAPIView(APIView):
    def get(self, request):
        userid = request.user.id
        if not models.UserMap.objects.filter(user_id=userid).exists():
            return Response({'code': 200, 'msg': '未点亮'}, status=status.HTTP_200_OK)
        else:
            return Response({'code': 200, 'msg': '已点亮', 'rank':models.UserMap.objects.get(user_id=userid).id}, status=status.HTTP_200_OK)


def count(request):
    if request.method == 'GET':
        number = models.UserMap.objects.all().count()
        return JsonResponse({'code': 200, 'number': number})
