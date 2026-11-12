from django.urls import path
from . import views

urlpatterns = [
    # paths for HTML

    path('image/', views.image, name = 'image'),
    path('video/', views.video, name = 'video'),

    # path for OpenCV tasks

    path('processImage/', views.upload_image, name = 'upload_image'),
    path('processVideo/', views.upload_video, name = 'video_processing')
]