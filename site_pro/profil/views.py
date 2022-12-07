from django.shortcuts import render
from profil.models import Profil
from project.models import Project


def home(request):
    
    profil = Profil.objects.first()
    projects = Project.objects.all()
    context = {
        'profil': profil,
        'projects': projects,
    }

    return render(request, 'profil/index.html', context=context)
