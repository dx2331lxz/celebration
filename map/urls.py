from django.urls import path
from . import views

urlpatterns = [
    path('province/', views.ProvinceAPIView.as_view()),
]
