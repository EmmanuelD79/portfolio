import pytest

from django.test import TestCase
from websnapbook.models import Event, Photo, Comment
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestEvent:
    pytestmark = pytest.mark.django_db

    def test_should_create_event_model(self):
        event = Event.objects.create(
            name='Test', date='2023-06-01', description='Ma description')
        expected_value = "Test"
        assert str(event) == expected_value
        assert Event.objects.count() == 1


class TestPhotoModel(TestCase):
    def setUp(self):
        # Création des objets nécessaires pour les tests
        self.event = Event.objects.create(
            name='Wedding', date='2023-06-01', description='Ma description')
        self.user = User.objects.create(username='testuser')
        self.photo = Photo.objects.create(
            event=self.event, uploader=self.user, image='test.jpg')

    def test_photo_creation(self):
        # Vérifie si l'objet Photo est créé correctement
        self.assertEqual(self.photo.event, self.event)
        self.assertEqual(self.photo.uploader, self.user)
        self.assertEqual(self.photo.image, 'test.jpg')
        self.assertIsNotNone(self.photo.uploaded_at)
        self.assertEqual(self.photo.likes.count(), 0)

    def test_photo_likes(self):
        # Vérifie si l'ajout et la suppression de likes fonctionnent correctement
        self.assertEqual(self.photo.likes.count(), 0)

        # Ajoute un like
        self.photo.likes.add(self.user)
        self.assertEqual(self.photo.likes.count(), 1)
        self.assertIn(self.user, self.photo.likes.all())

        # Supprime le like
        self.photo.likes.remove(self.user)
        self.assertEqual(self.photo.likes.count(), 0)
        self.assertNotIn(self.user, self.photo.likes.all())

    def test_photo_string_representation(self):
        # Vérifie si la méthode __str__ retourne une représentation appropriée
        expected_string = f'Photo uploaded by {self.user.username}'
        self.assertEqual(str(self.photo), expected_string)


class CommentModelTestCase(TestCase):
    def setUp(self):
        # Création des objets nécessaires pour les tests
        self.event = Event.objects.create(
            name='Wedding', date='2023-06-01', description='Ma description')
        self.user = User.objects.create(username='testuser')
        self.photo = Photo.objects.create(
            event=self.event, uploader=self.user, image='test.jpg')
        self.comment = Comment.objects.create(
            photo=self.photo, commenter=self.user, text='Great photo!')

    def test_comment_creation(self):
        # Vérifie si l'objet Comment est créé correctement
        self.assertEqual(self.comment.photo, self.photo)
        self.assertEqual(self.comment.commenter, self.user)
        self.assertEqual(self.comment.text, 'Great photo!')
        self.assertIsNotNone(self.comment.commented_at)

    def test_comment_string_representation(self):
        # Vérifie si la méthode __str__ retourne une représentation appropriée
        expected_string = f"Comment by {self.comment.commenter.username}"
        self.assertEqual(str(self.comment), expected_string)
