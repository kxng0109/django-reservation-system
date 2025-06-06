from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from django.http import HttpRequest
from .models import Reservation
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def make_reservation(request):
    form = ReservationForm()

    if(request.method == "POST"):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect(reservation_success)
    
    context = {
        'form': form,
    }
        
    return render(request, "make_reservation.html", context)

def reservation_success(request):
    return render(request, "reservation_success.html")

@staff_member_required
def reservation_list(request:HttpRequest):
    q = request.GET.get("q", "").strip()
    if(q):
        reservations = Reservation.objects.filter(
            Q(first_name__icontains = q) | Q(last_name__icontains = q)
        ).order_by('-date', '-created_at')
    else: 
        reservations = Reservation.objects.order_by("-date", "-created_at")
    
    context = {
        'reservations': reservations,
        'search_term': q
    }

    return render(request, 'reservation_list.html', context)

@staff_member_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    context = {
        "reservation": reservation
    }
    return render(request, "reservation_detail.html", context)

@staff_member_required
def reservation_edit(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if(request.method == "POST"):
        form = ReservationForm(request.POST, instance=reservation)
        if(form.is_valid()):
            form.save()
            return redirect(reservation_detail, pk=reservation.pk)
    else:
        form = ReservationForm(instance=reservation)

    context = {
        "form": form,
        "reservation": reservation
    }

    return render(request, 'reservation_form.html', context)

@staff_member_required
def reservation_delete (request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if(request.method == "POST"):
        reservation.delete()
        return redirect(reservation_list)
    else:
        context = {
            "reservation": reservation
        }
        return render(request, "reservation_delete_confirmation.html", context)
    