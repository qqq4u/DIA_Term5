from datetime import datetime

import requests

import random


from django.contrib.auth import authenticate
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.cache import cache

from .jwt_helper import *
from .permissions import *
from .serializers import *


def get_draft_ticket(request):
    token = get_access_token(request)

    if token is None:
        return None

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    ticket = Ticket.objects.filter(owner=user_id).filter(status=1).first()

    if ticket is None:
        return None

    return ticket


@api_view(["GET"])
def search_parkings(request):
    query = request.GET.get("query", "")

    parkings = Parking.objects.filter(status=1).filter(name__icontains=query)

    serializer = ParkingSerializer(parkings, many=True)

    draft_ticket = get_draft_ticket(request)

    resp = {
        "parkings": serializer.data,
        "draft_ticket": draft_ticket.pk if draft_ticket else None
    }

    return Response(resp)


@api_view(["GET"])
def get_parking_by_id(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)
    serializer = ParkingSerializer(parking, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_parking(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)
    serializer = ParkingSerializer(parking, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_parking(request):
    Parking.objects.create()

    parkings = Parking.objects.filter(status=1)
    serializer = ParkingSerializer(parkings, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_parking(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)
    parking.status = 5
    parking.save()

    parkings = Parking.objects.filter(status=1)
    serializer = ParkingSerializer(parkings, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_parking_to_ticket(request, parking_id):
    access_token = get_access_token(request)
    payload = get_jwt_payload(access_token)
    user_id = payload["user_id"]

    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)

    ticket = get_draft_ticket(request)

    if ticket is None:
        ticket = Ticket.objects.create()

    if ticket.parkings.contains(parking):
        return Response(status=status.HTTP_409_CONFLICT)

    ticket.parkings.add(parking)
    ticket.user = CustomUser.objects.get(pk=user_id)
    ticket.save()

    serializer = ParkingSerializer(ticket.parkings, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_parking_image(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)

    return HttpResponse(parking.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_parking_image(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)
    serializer = ParkingSerializer(parking, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_tickets(request):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user = CustomUser.objects.get(pk=payload["user_id"])

    status_id = int(request.GET.get("status", -1))
    date_start = int(request.GET.get("date_start", -1))
    date_end = int(request.GET.get("date_end", -1))

    tickets = Ticket.objects.exclude(status__in=[1, 5]) if user.is_moderator else Ticket.objects.filter(
        owner_id=user.pk)

    if status_id != -1:
        tickets = tickets.filter(status=status_id)

    if date_start != -1:
        tickets = tickets.filter(date_of_formation__gt=datetime.fromtimestamp(date_start).date())

    if date_end != -1:
        tickets = tickets.filter(date_of_formation__lt=datetime.fromtimestamp(date_end).date())

    serializer = TicketSerializer(tickets, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_ticket_by_id(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    serializer = TicketSerializer(ticket, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_ticket(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    serializer = TicketSerializer(ticket, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteWebService])
def update_ticket_time_entry(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)

    time_entry = request.data.get("time", "")
    if not ticket:
        ticket.time_entry = 0
        ticket.status = 3
        ticket.save()
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket.time_entry = time_entry
    ticket.time_entry_status = 4
    ticket.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)

    ticket.status = 2
    ticket.date_of_formation = datetime.now()
    ticket.save()

    calculate_ticket_time_entry(ticket.pk)

    serializer = TicketSerializer(ticket, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in ["3", "4"]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    ticket = Ticket.objects.get(pk=ticket_id)

    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user = CustomUser.objects.get(pk=payload["user_id"])

    ticket.status = request_status
    ticket.moderator = user
    ticket.date_complete = timezone.now()
    ticket.save()

    serializer = TicketSerializer(ticket, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_ticket(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)

    if ticket.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    ticket.status = 5
    ticket.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_parking_from_ticket(request, ticket_id, parking_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.parkings.remove(Parking.objects.get(pk=parking_id))
    ticket.save()

    serializer = ParkingSerializer(ticket.parkings, many=True)

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def check(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response


def calculate_ticket_time_entry(ticket_id):
    data = {
        "ticket_id": ticket_id,
    }

    requests.post("http://127.0.0.1:8080/calc_time/", json=data, timeout=3)
