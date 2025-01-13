from django.urls import path
from . import views

urlpatterns = [
    path('start_camera/', views.start_camera, name='start_camera'),
]
