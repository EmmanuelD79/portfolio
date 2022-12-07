from django.contrib import admin
from django.urls import path
from profil.views import home
from django.conf import settings
from django.conf.urls.static import static
from project.views import project
from contact.views import contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('<int:pk>', project, name='view_project'),
    path('contact/', contact, name='contact'),
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
