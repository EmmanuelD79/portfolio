from django import forms
from .models import Photo, Comment, Event, Guest
from django.contrib.auth import authenticate, login


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        labels = {'image': 'Choisir une photo'}
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Ajouter un commentaire'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1})
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'description']
        labels = {
            'name': 'Nom',
            'date': 'Date',
            'description': 'Description',
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Ton email'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email:
            user = Guest.authenticate_by_email(email)
            if user is None:
                raise forms.ValidationError("Vous n'êtes pas dans la liste des invités !")

        return cleaned_data


class GuestForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Nom d'utilisateur")

    class Meta:
        model = Guest
        fields = ['email', 'username']
