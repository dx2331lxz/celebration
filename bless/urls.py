from django.urls import path
from . import views

urlpatterns = [
    path('bless/', views.BlessAPIView.as_view()),
    path('discuss/', views.DiscussAPIView.as_view()),
    path('comment/', views.CommentAPIView.as_view()),
    path('like/', views.LikeAPIView.as_view()),
    path('image/', views.ImageAPIView.as_view()),
]
