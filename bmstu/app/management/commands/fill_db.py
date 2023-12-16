import random

from django.core import management
from django.core.management.base import BaseCommand
from app.models import *
from .utils import random_date, random_timedelta


def add_parkings():
    Parking.objects.create(
        name="Парковка возле главного здания",
        address="2-я Бауманская ул., 5, стр. 4, Москва",
        places_count=50,
        image="parkings/1.png"
    )

    Parking.objects.create(
        name="Парковка возле лефортовского тоннеля",
        address="Кондрашёвский тупик, 3А, Москва",
        places_count=150,
        image="parkings/2.png"
    )

    Parking.objects.create(
        name="Парковка возле корпуса Энергомашиностроения",
        address="Бригадирский пер., 3-5, Москва",
        places_count=30,
        image="parkings/3.png"
    )

    Parking.objects.create(
        name="Парковка возле УЛК",
        address="Рубцовская набережная, 2/18, Москва",
        places_count=20,
        image="parkings/4.png"
    )

    print("Услуги добавлены")


def add_tickets():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    parkings = Parking.objects.all()

    for _ in range(30):
        ticket = Ticket.objects.create()
        ticket.name = "Абонемент №" + str(ticket.pk)
        ticket.status = random.randint(2, 5)

        if ticket.status in [3, 4]:
            ticket.closed_date = random_date()
            ticket.formated_date = ticket.closed_date - random_timedelta()
            ticket.created_date = ticket.formated_date - random_timedelta()
            ticket.moderator = random.choice(moderators)
        else:
            ticket.formated_date = random_date()
            ticket.created_date = ticket.formated_date - random_timedelta()

        ticket.owner = random.choice(owners)

        for i in range(random.randint(1, 3)):
            ticket.parkings.add(random.choice(parkings))

        ticket.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")

        add_parkings()
        add_tickets()









