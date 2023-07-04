from django.urls import path
from websnapbook.views import create_event_view, event_detail_view, upload_photo, add_comment, like_photo, photo_detail_view, login_view, index_view, event_photos_view

app_name = 'websnapbook'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('create_event/', create_event_view, name='create_event'),
    path('event/<str:token>/', event_detail_view, name='event_detail'),
    path('event/<str:token>/photos/', event_photos_view, name='event_photos'),
    path('photo_detail/<int:photo_id>/', photo_detail_view, name='photo_detail'),
    path('upload_photo/<str:token>/', upload_photo, name='upload_photo'),
    path('add_comment/<int:photo_id>/', add_comment, name='add_comment'),
    path('like_photo/<int:photo_id>/', like_photo, name='like_photo'),
    path('', index_view, name='index'),
]
