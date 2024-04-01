from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.StudentAuthenticatedAPIView.as_view()),
    path('teacher/', views.TeacherAuthenticatedAPIView.as_view()),
    path('profession/', views.ProfessionalAPIView.as_view()),
    path('verification/', views.AuthenticationAPIView.as_view()),

]

