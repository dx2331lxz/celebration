from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('avatar/', views.AvatarAPIView.as_view()),
    path('nickname/', views.NicknameAPIView.as_view()),
    path('phone/', views.PhoneAPIView.as_view()),
    path('email/', views.EmailAPIView.as_view()),
    path('description/', views.DescriptionAPIView.as_view()),
    path('info/', views.InfoAPIView.as_view()),
]
