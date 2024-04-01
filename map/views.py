from django.shortcuts import render, HttpResponse
from . import  models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, pagination  # 状态和分页
import json
import os
from celebration import settings
import requests

class ProvinceAPIView(APIView):
    def get(self, request):
        lon = request.query_params.get('lon')
        lat = request.query_params.get('lat')
        if not lon or not lat:
            return Response({'code': 403, 'msg': '缺少参数'}, status=status.HTTP_403_FORBIDDEN)
        mapurl = f"http://api.tianditu.gov.cn/geocoder?postStr={{'lon':{lon},'lat':{lat},'ver':1}}&type=geocode&tk={settings.map_apikey}"
        response = requests.get(mapurl)

        return Response(response.json())
