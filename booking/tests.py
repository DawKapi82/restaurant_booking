from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory, Client
import os
from django.conf import settings
from django.test.utils import setup_test_environment

# from booking.views import *
# Create your tests here.
from booking.models import Reservation


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # os.environ['DJANGO_SETTINGS_MODULE'] = 'restaurant_booking.settings'
        # self.factory = RequestFactory()

    def test_index_without_msg(self):
        response = self.client.get('/booking/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_index_with_msg(self):
        session = self.client.session
        session['msg'] = "test123"
        session.save()

        response = self.client.get('/booking/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["msg"], 'test123')


class ReservationsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_reservations_staff(self):
        self.client.login(username="admin", password="Admin1.")
        response = self.client.get('/booking/reservations', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_reservations_not_staff(self):
        response = self.client.get('/booking/reservations')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/booking')


class AddReservationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_add_reservation_post_success(self):
        self.client.login(username='testuser', password='12345')

        form_data = {
            'user': '1',
            'name': 'Jan',
            'surname': 'Kowalski',
            'phone': '+48797654123',
            'reservation_date': '2023-06-11 11:00:00',
            'table_count': 2
        }
        response = self.client.post('/booking/add_reservation', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/booking/user_reservations')
        self.assertTrue(Reservation.objects.filter(reservation_date='2023-06-11 11:00:00').exists())

    def test_add_reservation_get_success(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/booking/add_reservation')
        self.assertEqual(response.status_code, 200)


class DeleteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser', is_staff=True)
        self.user.set_password('12345')
        self.user.save()

    def test_staff_delete(self):
        self.client.login(username='testuser', password='12345')

        reservation = Reservation.objects.create(
            id=1,
            user=1,
            name='John',
            surname='Kowalski',
            phone='+48797654123',
            reservation_date='2023-06-11 11:00:00',
            table_count=2
        )
        response = self.client.get('/booking/delete/' + str(reservation.id))
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())
        self.assertRedirects(response, '/booking/reservations')

    def test_non_staff_delete(self):
        reservation = Reservation.objects.create(
            id=1,
            user=1,
            name='John',
            surname='Kowalski',
            phone='+48797654123',
            reservation_date='2023-06-11 11:00:00',
            table_count=2
        )
        response = self.client.get('/booking/delete/' + str(reservation.id), follow=True)
        self.assertTrue(Reservation.objects.filter(id=reservation.id).exists())
        self.assertRedirects(response, '/booking/')


class UserReservationsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_logged_user_reservations(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/booking/user_reservations')
        self.assertEqual(response.status_code, 200)

    def test_non_logged_user_reservations(self):
        response = self.client.get('/booking/user_reservations', follow=True)
        self.assertRedirects(response, '/booking/login?next=/booking/user_reservations')


class CancelTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_logged_user_cancel(self):
        self.client.login(username='testuser', password='12345')

        reservation = Reservation.objects.create(
            id=1,
            user=1,
            name='John',
            surname='Kowalski',
            phone='+48797654123',
            reservation_date='2023-06-11 11:00:00',
            table_count=2
        )
        response = self.client.get('/booking/cancel/' + str(reservation.id))
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())
        self.assertRedirects(response, '/booking/user_reservations')

    def test_non_logged_user_cancel(self):
        reservation = Reservation.objects.create(
            id=1,
            user=1,
            name='John',
            surname='Kowalski',
            phone='+48797654123',
            reservation_date='2023-06-11 11:00:00',
            table_count=2
        )
        response = self.client.get('/booking/cancel/' + str(reservation.id))
        self.assertTrue(Reservation.objects.filter(id=reservation.id).exists())
        self.assertRedirects(response, '/booking/login?next=/booking/cancel/1')


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_correct_user_login(self):
        form_data = {
            'login': 'testuser',
            'password': '12345'
        }
        response = self.client.post('/booking/login', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/booking')

    def test_incorrect_user_login(self):
        form_data = {
            'login': 'testuser',
            'password': '123456'
        }
        response = self.client.post('/booking/login', data=form_data)
        self.assertEqual(response.status_code, 200)


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register(self):
        form_data = {
            'username': 'newuser',
            'password1': 'testy1234',
            'password2': 'testy1234'
        }
        response = self.client.post('/booking/register', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        

class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/booking/logout')
        self.assertFalse(response.wsgi_request.user.is_authenticated)
