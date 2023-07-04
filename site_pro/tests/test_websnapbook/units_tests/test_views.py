from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from websnapbook.views import login_view
from websnapbook.forms import EventForm, CustomAuthenticationForm
from websnapbook.models import Event


class CreateEventViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('websnapbook:create_event')
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_create_event_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'websnapbook/create_event.html')
        self.assertIsInstance(response.context['form'], EventForm)

    def test_create_event_view_with_unauthenticated_user(self):
        response = self.client.post(
            reverse('websnapbook:create_event'), follow=True)
        # Assert redirect to login page
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, '/websnapbook/login/?next=/websnapbook/create_event/')

    def test_create_event_view_post_valid_form(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'name': 'Mon événement',
            'date': '2023-01-01',
            'description': 'Une description d\'événement',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'websnapbook:event_detail', kwargs={'event_id': 1}))
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.name, 'Mon événement')
        self.assertEqual(str(event.date), '2023-01-01')
        self.assertEqual(event.description, 'Une description d\'événement')

    def test_create_event_view_post_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'name': '',
            'date': '2023-01-01',
            'description': 'Une description d\'événement',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'websnapbook/create_event.html')
        self.assertIsInstance(response.context['form'], EventForm)
        self.assertFormError(response, 'form', 'name',
                             'Ce champ est obligatoire.')


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('websnapbook:login')

    def test_login_get_request(self):
        # Envoie une requête GET à la vue de connexion
        response = self.client.get(self.login_url)

        # Vérifie que la réponse a un statut 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Vérifie que le formulaire dans le contexte est une instance d'AuthenticationForm
        self.assertIsInstance(response.context['form'], CustomAuthenticationForm)

    def test_login_post_request_valid_credentials(self):
        # Crée un utilisateur de test
        user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Envoie une requête POST à la vue de connexion avec des identifiants valides
        response = self.client.post(
            self.login_url, {'username': 'testuser', 'password': 'testpassword'})

        # Vérifie que la réponse redirige vers la page d'index
        self.assertRedirects(response, reverse('websnapbook:index'))

        # Vérifie que l'utilisateur est connecté
        self.assertTrue(user.is_authenticated)


    def test_login_post_request_invalid_credentials(self):
        # Envoie une requête POST à la vue de connexion avec des identifiants invalides
        response = self.client.post(
            self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'}, follow=True)

        # Vérifie que la réponse redirige vers la page de connexion (statut 200)
        self.assertEqual(response.status_code, 200)

        # Vérifie que le formulaire contient une erreur
        form = response.context['form']
        self.assertTrue(form.errors)

        # Vérifie que l'erreur est liée aux identifiants invalides
        self.assertEqual(form.errors['__all__'], ["Saisissez un nom d’utilisateur et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules)."])

        # Vérifie que l'utilisateur n'est pas connecté
        self.assertFalse(response.context['user'].is_authenticated)
