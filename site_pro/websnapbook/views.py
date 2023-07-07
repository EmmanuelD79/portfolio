from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import EventForm, CommentForm, PhotoForm, CustomAuthenticationForm, GuestForm
from .models import Event, Photo, Guest
from .assets.get_guest import get_event_guests
from .assets.get_token import generate_unique_token
from django.contrib.sites.shortcuts import get_current_site
from .assets.get_qrcode import generate_qrcode
from .wrappers import guest_required
from .assets.custom_login import GuestBackend


@login_required(login_url="/admin")
def create_event_view(request):
    current_site = get_current_site(request)
    hostname = current_site.domain
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            token = generate_unique_token(Event)
            event.token = token
            event.owner = request.user
            qrcode_url = hostname + '/websnapbook/event/' + token
            filepath = generate_qrcode(qrcode_url, token)
            event.qrcode = filepath
            event.save()

            # Faire quelque chose avec l'événement créé
            return redirect('websnapbook:event_detail', token=token)
    else:
        form = EventForm()

    context = {
        'form': form,
    }
    return render(request, 'websnapbook/create_event.html', context)


@guest_required(redirect_to="/websnapbook/login/")
def event_detail_view(request, token):
    event = Event.objects.get(token=token)
    guests = get_event_guests(event.id)
    guest_token = generate_unique_token(Guest)
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            try:
                guest = Guest.objects.get(email=email)
                if event.id not in guest.events.values_list('id', flat=True):
                    event = Event.objects.get(id=event.id)
                    guest.events.add(event)
            except Guest.DoesNotExist:
                guest = Guest.objects.create_user(
                    email=email, username=username, token=guest_token)
                guest.events.add(event.id)
            return redirect('websnapbook:event_detail', token=token)
    else:
        form = GuestForm()

    context = {
        'event': event,
        'form': form,
        'guests': guests,
    }
    return render(request, 'websnapbook/event_detail.html', context)


@guest_required(redirect_to="/websnapbook/login/")
def event_photos_view(request, token):
    event = Event.objects.get(token=token)
    photos = Photo.objects.filter(event=event)
    context = {
        'event': event,
        'photos': photos
    }
    return render(request, 'websnapbook/event_photos.html', context)


@guest_required(redirect_to="/websnapbook/login/")
def photo_detail_view(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.commenter = request.user
            comment.save()
            return redirect('websnapbook:photo_detail', photo_id=photo.id)
    else:
        form = CommentForm()
    context = {
        'photo': photo,
        'form': form,
    }
    return render(request, 'websnapbook/photo_detail.html', context)


@guest_required(redirect_to="/websnapbook/login/")
def upload_photo(request, token):
    event = Event.objects.get(token=token)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            for file_field in request.FILES.getlist('image'):
                photo = Photo(event=event, uploader=request.user)
                photo.image = file_field
                photo.save()
            return redirect('websnapbook:upload_photo', token=token)
    else:
        form = PhotoForm()
    context = {
        'form': form,
        'event': event,
        'token': token
    }
    return render(request, 'websnapbook/upload_photo.html', context)



@guest_required(redirect_to="/websnapbook/login/")
def add_comment(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.commenter = request.user
            comment.save()
            return redirect('websnapbook:event_detail', event_id=photo.event.id)
    else:
        form = CommentForm()
    context = {
        'form': form,
        'photo': photo
    }
    return render(request, 'websnapbook/add_comment.html', context)


@guest_required(redirect_to="/websnapbook/login/")
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.user.is_authenticated:
        #     if request.method == 'POST':
        photo.toggle_like(request.user)
        return redirect('websnapbook:photo_detail', photo_id=photo.id)
    else:
        # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = authenticate(request, email=email)
            if user is not None:
                login(request, user)
                redirect_to = request.GET.get('next', reverse('websnapbook:index'))
                return redirect(redirect_to)
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'websnapbook/login.html', context)


# @login_required(login_url="/websnapbook/login/")
@guest_required(redirect_to="/websnapbook/login/")
def index_view(request):
    
    guest = Guest.objects.get(email=request.user.email)
    events = guest.events.all()
    
    context = {
        'events': events,
    }
    
    return render(request, 'websnapbook/index.html', context)
