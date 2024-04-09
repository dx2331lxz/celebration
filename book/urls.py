from django.urls import path
from . import views

urlpatterns = [
    path('address/', views.AddressAPIView.as_view()),
    path('info/', views.InfoAPIView.as_view()),
]
