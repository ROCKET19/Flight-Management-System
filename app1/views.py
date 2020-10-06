from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
# Create your views here.
from .models import App1, Passenger
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


def index(request):
    if not request.user.is_authenticated:
        return render(request, "app1/home.html", {"message": None})
    context = {
        "app1": App1.objects.all(),
        "user": request.user
    }
    return render(request, "app1/index.html", context)


def flight(request, flight_id):
    try:
        flight = App1.objects.get(pk=flight_id)
    except App1.DoesNotExist:
        raise Http404("Flight Does not exist.")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "app1/app1.html", context)


def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = App1.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "app1/error.html", {"message": "No selection done."})
    except App1.DoesNotExist:
        return render(request, "app1/error.html", {"message": "No Flight."})
    except Passenger.DoesNotExist:
        return render(request, "app1/error.html", {"message": "No Passenger."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if request.user.is_authenticated:
        logout(request)
        return render(request, "app1/index.html", {"message": None})
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app1/home.html", {"message": "Invalid Credentials"})


def logout_view(request):
    logout(request)
    return render(request, "app1/home.html", {"message": None})
