from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('parkings/<int:parking_id>', parking_details, name="parking_details"),
    path('parkings/<int:parking_id>/delete/', parking_delete, name="parking_delete")
]
