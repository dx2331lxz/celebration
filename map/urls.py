from django.urls import path
from . import views

urlpatterns = [
    path('light/', views.LightAPIView.as_view()),
    path('rank/', views.RankAPIView.as_view()),
    path('verify/', views.GoHomeAPIView.as_view()),
    path('count/', views.count),
]
