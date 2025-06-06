from django.urls import path
from .views import make_reservation, reservation_success, reservation_list, reservation_detail, reservation_edit, reservation_delete

urlpatterns = [
    path("reserve/", make_reservation, name="make_reservation"),
    path("reserve/success", reservation_success, name="reservation_success"),
    path("reservations/list", reservation_list, name="reservation_list"),
    path("reservation/<int:pk>", reservation_detail, name="reservation_detail"),
    path("reservation/<int:pk>/edit", reservation_edit, name="reservation_edit"),
    path("reservation/<int:pk>/delete", reservation_delete, name="reservation_delete")
]