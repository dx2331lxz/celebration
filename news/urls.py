from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsAPIView.as_view()),
    path('news/<int:id>/', views.NewsDetailAPIView.as_view()),
    path('activity/', views.ActivityAPIView.as_view()),
    path('activity/<int:id>/', views.ActivityDetailAPIView.as_view()),
]
