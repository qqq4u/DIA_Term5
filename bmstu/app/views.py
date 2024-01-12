from datetime import datetime

import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_ticket(request):
    user = identity_user(request)

    if user is None:
        return None

    ticket = Ticket.objects.filter(owner=user).filter(status=1).first()

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
        "draft_ticket_id": draft_ticket.pk if draft_ticket else None
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
    serializer = ParkingSerializer(parking, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_parking(request):
    parking = Parking.objects.create()

    serializer = ParkingSerializer(parking)

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
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)

    ticket = get_draft_ticket(request)

    if ticket is None:
        ticket = Ticket.objects.create()

    if ticket.parkings.contains(parking):
        return Response(status=status.HTTP_409_CONFLICT)

    ticket.parkings.add(parking)
    ticket.owner = identity_user(request)
    ticket.save()

    serializer = TicketSerializer(ticket)

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
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start", -1)
    date_end = request.GET.get("date_end", -1)

    tickets = Ticket.objects.exclude(status__in=[1, 5]) 
    
    if not user.is_moderator:
        tickets = tickets.filter(owner=user)

    if status_id > 0:
        tickets = tickets.filter(status=status_id)

    if date_start:
        tickets = tickets.filter(date_formation__gte=parse_datetime(date_start))

    if date_end:
        tickets = tickets.filter(date_formation__lte=parse_datetime(date_end))

    serializer = TicketsSerializer(tickets, many=True)

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
@permission_classes([IsRemoteService])
def update_ticket_entry_time(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)

    raw_time = request.data.get("time")
    if raw_time == "":
        return Response(status=status.HTTP_400_BAD_REQUEST)

    ticket.entry_time = datetime.strptime(raw_time, '%Y-%m-%d %H:%M:%S')
    ticket.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)

    ticket.status = 2
    ticket.date_formation = timezone.now()
    ticket.save()

    calculate_entry_time(ticket_id)

    serializer = TicketSerializer(ticket, many=False)

    return Response(serializer.data)


def calculate_entry_time(ticket_id):
    data = {
        "ticket_id": ticket_id
    }

    requests.post("http://127.0.0.1:8080/calc_time/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    ticket = Ticket.objects.get(pk=ticket_id)

    if ticket.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    ticket.status = request_status
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

    serializer = TicketSerializer(ticket)

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
