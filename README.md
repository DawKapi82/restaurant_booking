# Restaurant Booking System

## Target of the project

System was designed for creating bookings for tables in restaurant and managing bookings by users.
Users have possibility to log in into application and create and cancel the reservations.
Admin can view all reservations and manage them.bookings

## Technology stack

Main system logic is written in python django. Data is stored in SQLite database. Front-end part is using HTML with bootstrap library.

## Python code

### Core logic

Application logic is stored in views.py file where the requests are processed.

```python

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

```

Method processing creating reservation

### Testing

All view methods are tested in tests.py

```python

class ReservationsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_reservations_staff(self):
        self.client.login(username="admin",password="Admin1.")
        response = self.client.get('/booking/reservations', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_reservations_not_staff(self):
        response = self.client.get('/booking/reservations')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/booking')

```

Test case for Resersvations view

## HTML templates

Templates for front-end of application are in templates folder. Written in HTML with bootstrap libriaries

```html

{% extends "layout.html" %}

{% block content %}

<form action="/booking/add_reservation" method="post">
    {% csrf_token %}
    <div class="m-3">
    {{ form }}
    </div>
    <div class="m-3">
        <button type="submit" class="btn btn-primary">Save</button>
    </div>
</form>

{% endblock content %}

```

