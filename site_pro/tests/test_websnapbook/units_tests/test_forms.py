from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
from io import BytesIO
from websnapbook.forms import PhotoForm, CommentForm, EventForm
from django.contrib.auth.models import User
from websnapbook.models import Comment


class PhotoFormTestCase(TestCase):
    def test_photo_form_valid(self):
        # Crée une image noire
        image = Image.new('RGB', (100, 100), color='black')
        image_bytes = BytesIO()
        image.save(image_bytes, 'JPEG')
        image_bytes.seek(0)

        # Crée un fichier temporaire avec l'image noire
        uploaded_file = SimpleUploadedFile(
            'test.jpg', image_bytes.read(), content_type='image/jpeg')

        # Utilise le fichier temporaire dans le formulaire
        form = PhotoForm(data={}, files={'image': uploaded_file})

        # Vérifie si le formulaire est valide
        self.assertTrue(form.is_valid(), form.errors)

    def test_photo_form_invalid(self):
        # Crée une instance de formulaire avec des données invalides
        form = PhotoForm(data={})

        # Vérifie si le formulaire est invalide
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('image', form.errors)
        self.assertEqual(form.errors['image'][0], 'Ce champ est obligatoire.')


class CommentFormTestCase(TestCase):
    def test_comment_form_valid(self):
        form_data = {'text': 'Ceci est un commentaire.'}
        form = CommentForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_comment_form_empty(self):
        form_data = {}
        form = CommentForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('text', form.errors)
        self.assertEqual(form.errors['text'][0], 'Ce champ est obligatoire.')

    def test_comment_form_max_length(self):
        max_length = Comment._meta.get_field('text').max_length
        long_text = 'A' * (max_length + 1)
        form_data = {'text': long_text}
        form = CommentForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('text', form.errors)
        self.assertEqual(
            form.errors['text'][0], f'Assurez-vous que cette valeur comporte au plus {max_length} caractères (actuellement {len(long_text)}).')


class EventFormTestCase(TestCase):
    def test_event_form_valid(self):
        form_data = {
            'name': 'Mon événement',
            'date': '2023-06-01',
            'description': 'Une description d\'événement',
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_event_form_invalid(self):
        form_data = {
            'name': '',
            'date': '2023-06-01',
            'description': 'Une description d\'événement',
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('name', form.errors)
