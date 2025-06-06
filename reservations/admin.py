from django.contrib import admin
from .models import Reservation

# Register your models here.

class ReservationModel(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date', 'party_size', 'created_at')
    list_filter = ('date',)
    search_fields = ('name', 'notes')

admin.site.register(Reservation, ReservationModel)