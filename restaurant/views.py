# from django.http import HttpResponse
import json
from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .forms import BookingForm, ReservationForm
from .models import Menu, Reservation
from .serializers import UserSerializer, MenuSerializer, ReservationSerializer


# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)


def reserve(request):
    form = ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'reserve.html', context)


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)
        exist = Reservation.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()

        if not exist:
            booking = Reservation(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error': 1}", content_type='application/json')
    date = request.GET.get('date', default=datetime.today().date())
    bookings = Reservation.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    return HttpResponse(booking_json, content_type='application/json')


def reservations(request):
    bookings = Reservation.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'reservations.html', {"bookings": booking_json})


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {'Menu': menu_data}
    return render(request, 'menu.html', main_data)


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    return render(request, 'menu_item.html', {'menu_item': menu_item})


class UserView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
