from django.contrib import admin
from message.models import Reservation, History, Room

# Register your models here.
admin.site.register(Reservation)
admin.site.register(History)
admin.site.register(Room)
