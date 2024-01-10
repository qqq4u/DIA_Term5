from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Ticket.objects.all().delete()
        Parking.objects.all().delete()
        CustomUser.objects.all().delete()