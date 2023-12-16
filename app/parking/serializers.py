from rest_framework import serializers

from .models import *


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    parkings = ParkingSerializer(read_only=True, many=True)

    class Meta:
        model = Ticket
        fields = '__all__'