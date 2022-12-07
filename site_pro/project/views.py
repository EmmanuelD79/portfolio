from django.shortcuts import render
from project.models import Project
from profil.models import Profil


def project(request, pk):
    
    project = Project.objects.get(pk=pk)
    profil = Profil.objects.first()
    
    context = {
        'project': project,
        'profil': profil
    }

    return render(request, 'project/index.html', context=context)
