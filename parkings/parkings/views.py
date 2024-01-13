from django.shortcuts import render

from parkings.utils.db import *


def index(request):
    query = request.GET.get("parkings")
    parkings = searchParkings(query) if query else getParkings()

    context = {
        "parkings": parkings,
        "search_query": query if query else ""
    }

    return render(request, "home_page.html", context)


def parkingOrderPage(request, parking_id):
    parking = getParkingById(parking_id)

    context = {
        "username": "Админ",
        "parking_id": parking_id,
        "parking_name": parking["parking_name"],
        "parking_adress": parking["parking_adress"],
        "parking_places_count": parking["parking_places_count"],
    }

    return render(request, "order_page.html", context)
