from django.urls import path
from .views import make_reservation

urlpatterns = [
    path("reserve/", make_reservation, name="make_reservation")
]