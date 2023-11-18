from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *


def get_draft_ticket():
    ticket = Ticket.objects.filter(status=1).first()

    if ticket is None:
        return None

    serializer = TicketSerializer(ticket, many=False)
    return serializer.data


@api_view(["GET"])
def search_parking(request):
    name = request.GET.get('query', '')

    parking = Parking.objects.filter(status=1).filter(name__icontains=name)

    serializer = ParkingSerializer(parking, many=True)

    data = {
        "parkings": serializer.data,
        "draft_ticket": get_draft_ticket()
    }

    return Response(data)


@api_view(['GET'])
def get_parking_by_id(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Получение данные после запроса с БД (через ORM)
    parking = Parking.objects.get(pk=parking_id)

    serializer = ParkingSerializer(parking, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_parking(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)
    serializer = ParkingSerializer(parking, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_parking(request):
    Parking.objects.create()

    parkings = Parking.objects.all()
    serializer = ParkingSerializer(parkings, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_parking(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)
    parking.status = 2
    parking.save()

    parkings = Parking.objects.filter(status=1)
    serializer = TicketSerializer(parkings, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_parking_to_ticket(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)

    ticket = Ticket.objects.filter(status=1).last()

    if ticket is None:
        ticket = Ticket.objects.create()

    ticket.parkings.add(parking)
    ticket.save()

    serializer = ParkingSerializer(ticket.parkings, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_parking_image(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Parking.objects.get(pk=parking_id)

    return HttpResponse(service.image, content_type="image/png")


@api_view(["PUT"])
def update_parking_image(request, parking_id):
    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    parking = Parking.objects.get(pk=parking_id)
    serializer = ParkingSerializer(parking, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def get_tickets(request):
    tickets = Ticket.objects.all()

    request_status = request.GET.get("status")
    if request_status:
        tickets = tickets.filter(status=request_status)

    serializer = TicketSerializer(tickets, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_ticket_by_id(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    serializer = TicketSerializer(ticket, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_ticket(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    serializer = TicketSerializer(ticket, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    ticket.status = 1
    ticket.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.status = 2
    ticket.save()

    serializer = TicketSerializer(ticket, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    ticket = Ticket.objects.get(pk=ticket_id)

    ticket_status = ticket.status

    if ticket_status in [3, 4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    ticket.status = request_status
    ticket.save()

    serializer = TicketSerializer(ticket, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_ticket(request, ticket_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.status = 5
    ticket.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_parking_from_ticket(request, ticket_id, parking_id):
    if not Ticket.objects.filter(pk=ticket_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Parking.objects.filter(pk=parking_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.parkings.remove(Ticket.objects.get(pk=parking_id))
    ticket.save()

    serializer = ParkingSerializer(ticket.parkings, many=True)

    return Response(serializer.data)

