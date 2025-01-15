from django.urls import path
from . import views

urlpatterns = [
    path('start_camera/', views.start_camera, name='start_camera'),
    path('stop_camera/', views.stop_camera, name='stop_camera'),
]
