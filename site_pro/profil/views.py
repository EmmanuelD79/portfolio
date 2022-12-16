from django.shortcuts import render, redirect
from profil.models import Profil
from project.models import Project
from django.urls import reverse


def home(request, slug):

    profil = Profil.objects.get(custom_url=slug)
    projects = Project.objects.filter(user=profil)
    context = {
        'profil': profil,
        'projects': projects,
    }

    return render(request, 'profil/index.html', context=context)


def index(resquest, slug):
    return redirect(reverse('profil:home', kwargs={'slug': slug}))


def error_404_view(request, exception):
    return render(request, '404.html')

def error_500_view(request):
    return render(request, '500.html')


def base(request):

    context = {
        'profil': None,
        'projects': None,
    }
    return render(request, 'profil/index.html', context=context)
