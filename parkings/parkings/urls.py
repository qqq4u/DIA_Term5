from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('parking/<int:parking_id>', parkingOrderPage, name="parking")
]