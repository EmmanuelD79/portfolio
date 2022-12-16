from django.shortcuts import render
from project.models import Project
from profil.models import Profil


def project(request, project_slug, slug):

    profil = Profil.objects.get(custom_url=slug)
    project = Project.objects.filter(user=profil).get(project_slug=project_slug)
    
    context = {
        'project': project,
        'profil': profil
    }

    return render(request, 'project/index.html', context=context)
