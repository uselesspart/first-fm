from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index),
    path("search/", views.search),
    path('result/', views.result, name='result'),
    path('add-album/', views.add_album, name='add_album'),
    path('add-artist/', views.add_artist, name='add_artist'),
    path('success/', views.success, name='success'),
    path('artist-page/', views.artist_page, name='artist_page'),
    path('album-page/', views.album_page, name='album_page'),
    path('genre-page/', views.genre_page, name='genre_page'),
]