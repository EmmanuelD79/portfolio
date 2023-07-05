from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profil.views import base


urlpatterns = [
    path('admin/', admin.site.urls),
    path('websnapbook/', include('websnapbook.urls')),
    path('<slug:slug>/', include('profil.urls')),
    path('', base, name='view_base'),
]

handler500 = 'profil.views.error_500_view'

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
