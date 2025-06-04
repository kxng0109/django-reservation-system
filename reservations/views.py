from django.shortcuts import render, redirect
from .forms import ReservationForm
from django.http import HttpResponse

# Create your views here.
def make_reservation(request):
    form = ReservationForm()

    if(request.method == "POST"):
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Success")
    
    context = {
        'form': form
    }
        
    return render(request, "make_reservation.html", context)