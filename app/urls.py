from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name='app'),
    path('search/', views.search, name='search'),
    path('result/', views.result, name='result'),
    path('add-album/', views.add_album, name='add_album'),
    path('add-artist/', views.add_artist, name='add_artist'),
    path('add-song/', views.add_song, name='add_song'),
    path('add-review/', views.add_review, name='add_review'),
    path('add-rating/', views.add_rating, name='add_rating'),
    path('add-like/', views.add_like, name='add_like'),
    path('add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('success/', views.success, name='success'),
    path('artist-page/', views.artist_page, name='artist_page'),
    path('album-page/', views.album_page, name='album_page'),
    path('genre-page/', views.genre_page, name='genre_page'),
    path('get-cover/', views.get_cover, name='get_cover'),
    path('get-picture/', views.get_picture, name='get_picture'),
    path('likes/', views.get_likes, name='get_likes'),
    path('favorites/', views.get_favorites, name='get_favorites'),
    path('img/', views.imgt, name='img'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)