from django.shortcuts import render, redirect

from .models import *


def index(request):
    query = request.GET.get("query")
    thematics = Parking.objects.filter(name__icontains=query).filter(status=1) if query else Parking.objects.filter(status=1)

    context = {
        "search_query": query if query else "",
        "parkings": thematics
    }

    return render(request, "home_page.html", context)


def parking_details(request, parking_id):
    context = {
        "parking": Parking.objects.get(id=parking_id)
    }

    return render(request, "parking_page.html", context)


def parking_delete(request, parking_id):
    parking = Parking.objects.get(id=parking_id)
    parking.delete()

    return redirect("/")
