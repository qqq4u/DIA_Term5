from django.contrib import admin
from .models import *


admin.site.register(CustomUser)
admin.site.register(Parking)
admin.site.register(Ticket)
