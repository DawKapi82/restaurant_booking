from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q

# Create your views here.
from booking.forms import ReservationForm, CustomUserCreationForm
from booking.models import Reservation


def index(request):
    msg = None
    if 'msg' in request.session:
        msg = request.session['msg']

    return render(request, 'index.html', {'msg': msg})


def reservations(request):
    if request.user.is_staff:
        context = {'reservations': Reservation.objects.all()}
        return render(request, 'reservations.html', context)
    else:
        return redirect('/booking')


@login_required()
def add_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        w = form.save(commit=False)
        w.user = request.user.id

        if Reservation.objects.filter(Q(reservation_date__year=w.reservation_date.year)
                                      & Q(reservation_date__month=w.reservation_date.month)
                                      & Q(reservation_date__day=w.reservation_date.day)
                                      & Q(user=str(request.user.id))).exists():
            request.session['msg'] = 'There is already reservation for this date.'
            return redirect('/booking')
        else:
            w.save()
            return redirect('/booking/user_reservations')
    else:
        form = ReservationForm()
        return render(request, 'reservation.html', {'form': form})


def delete(request, rid):
    if request.user.is_staff:
        Reservation.objects.filter(id=rid).delete()
    return redirect('/booking/reservations')


@login_required()
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user.id).order_by('reservation_date')
    return render(request, 'user_reservations.html', {'reservations': reservations})


@login_required()
def cancel(request, rid):
    reservation = Reservation.objects.get(id=rid)

    if reservation.reservation_date > timezone.now() and reservation.user == str(request.user.id):
        reservation.delete()

    return redirect('/booking/user_reservations')


def user_login(request):
    if request.method == "POST":
        username = request.POST["login"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'login.html')
        else:
            login(request, user)
            return redirect('/booking')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/booking/login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/booking')