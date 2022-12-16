from django.urls import path
from profil.views import home, index
from contact.views import contact
from project.views import project

app_name = 'profil'

urlpatterns = [
    path('project/<slug:project_slug>/', project, name='view_project'),
    path('contact/', contact, name='view_contact'),
    path('', home, name='home'),
    path('project/', index, name='index'),
]

handler404 = 'profil.views.error_404_view'
