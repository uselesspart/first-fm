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
    path('add-playlist', views.add_playlist, name='add_playlist'),
    path('add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('add-songs-playlist', views.add_songs_playlist, name='add_songs_playlist'),
    path('add-song-to-playlist', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('success/', views.success, name='success'),
    path('artist-page/', views.artist_page, name='artist_page'),
    path('delete-album/', views.delete_album, name='delete_album'),
    path('delete-artist/', views.delete_artist, name='delete_artist'),
    path('delete-song/', views.delete_song, name='delete_song'),
    path('reviews/', views.get_reviews, name='get_reviews'),
    path('album-page/', views.album_page, name='album_page'),
    path('genre-page/', views.genre_page, name='genre_page'),
    path('get-cover/', views.get_cover, name='get_cover'),
    path('get-picture/', views.get_picture, name='get_picture'),
    path('likes/', views.get_likes, name='get_likes'),
    path('playlists', views.get_playlists, name='get_playlists'),
    path('playlist', views.get_playlist, name='get_playlist'),
    path('favorites/', views.get_favorites, name='get_favorites'),
    path('img/', views.imgt, name='img'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)