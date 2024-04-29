from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os
import gridfs
import base64
from datetime import datetime
from django.db.models import Q
import requests
from django.conf import settings
import uuid

def success(request):
    return render(request, 'success.html')

def index(request):
    return render(request, 'app.html')

def search(request):
    genres = Genre.objects.all()
    return render(request, 'search.html', context={"genres": list(genres)})

def result(request):
    genres = list(Genre.objects.all())
    result = []
    res = []
    ys = request.POST.get('year-start')
    ye = request.POST.get('year-end') 
    for g in genres:
        if request.POST.get(g.name) == 'on':
            albums = list(AlbumGenre.objects.filter(genre_id=g.id))
            if albums != []:
                for a in albums:
                    res = list(Album.objects.filter(id=a.album_id, year__gte=ys, year__lte=ye))
                    if res != [] and not res in result:
                        result.append(res)
    artists = []
    data = []
    if result != []:
        for r in result:
            a = list(Artist.objects.filter(id=r[0].artist_id))
            if a != [] and not a in artists:
                a.append(artists)
                data.append([r, a])

    return render(request, 'result.html', context={"result": data})

def genre_page(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        g = list(Genre.objects.filter(name=genre))
        album_genres = list(AlbumGenre.objects.filter(genre_id=g[0].id))
        albums = []
        for album_g in album_genres:
            album = list(Album.objects.filter(id=album_g.album_id))
            if album != []:
                albums.append(album)
        return(render(request, 'genre_page.html', {'genre': g, 'albums': albums}))
    else:
        HttpResponseRedirect("../")
    return(render(request, 'genre_page.html', {'genre': genre}))    

def artist_page(request):
    if request.method == 'POST':
        artist = request.POST.get('artist')
        a = list(Artist.objects.filter(name=artist))
        albums = []
        al = Album.objects.filter(artist_id=a[0].id)
        fs = list(Favorite.objects.filter(artist_id=a[0].id))
        fans = []
        for f in fs:
            fans.append(f.user_id)
        return(render(request, 'artist_page.html', {'artist': a, 'albums': al, 'artist_id': a[0].id, 'fans': fans}))
    else:
        HttpResponseRedirect("../")
    return(render(request, 'artist_page.html', {'artist': artist}))

def album_page(request):
    if request.method == 'POST':
        album = request.POST.get('album')
        a = list(Album.objects.filter(name=album))
        artist = Artist.objects.filter(id=a[0].artist_id)
        year = a[0].year
        genres = list(Genre.objects.all())
        res = []
        for g in genres:
            r = list(AlbumGenre.objects.filter(album_id=a[0].id, genre_id=g.id))
            if r != []:
                res.append(g)
        songs = list(Song.objects.filter(album_id=a[0].id))
        durations = []
        for s in songs:
            seconds = s.duration % 60
            if seconds < 10:
                seconds = f'0{seconds}'
            durations.append([s, s.duration // 60, seconds, s.id])
        reviews = list(Review.objects.filter(album=a[0]))
        ratings = list(Rating.objects.filter(album=a[0]))
        rated = []
        rates = []
        for r in ratings:
            rated.append(r.user_id)
            rates.append([r.user_id, r])
        
        return(render(request, 'album_page.html', {'album': a, 'rates': rates, 'ratings': rated, 'durations': durations,'album_id': a[0].id,'data': [a, artist, year, res, reviews] }))
    else:
        HttpResponseRedirect("../")
    return(render(request, 'album_page.html', {'album': album}))

def get_cover(request):
    album_id = request.POST.get('album_id')
    cover_id = list(Album.objects.filter(id=album_id))[0].cover_id
    response = get_image(cover_id)
    return response

def get_reviews(request):
    user_id = request.POST.get('user_id')
    reviews = list(Review.objects.filter(user_id=user_id))
    data = []
    for review in reviews:
        data.append([review, Album.objects.get(id=review.album.id)])
    return render(request, 'reviews.html', {'data': data })

def get_picture(request):
    artist_id = request.POST.get('artist_id')
    picture_id = list(Artist.objects.filter(id=artist_id))[0].picture_id
    response = get_image(picture_id)
    return response

def add_rating(request):
    album_id = request.POST.get('album_id')
    value = request.POST.get('rating')
    user_id = request.POST.get('user_id')
    album = list(Album.objects.filter(id=album_id))
    rating = Rating(album_id=album_id, rating=value, user_id=user_id, created_at=datetime.now())
    rating.save()
    return HttpResponseRedirect("../search/")

def get_likes(request):
    user_id = request.POST.get('user_id')
    likes = list(Like.objects.filter(user_id=user_id))
    songs = []
    for like in likes:
        song = list(Song.objects.filter(id=like.song_id))
        if song != [] and song not in songs:
            artist_id = song[0].artist_id
            artist = list(Artist.objects.filter(id=artist_id))[0]
            songs.append([artist, song])
    return(render(request, 'likes.html', {'songs': songs}))

def get_favorites(request):
    user_id = request.POST.get('user_id')
    favorites = list(Favorite.objects.filter(user_id=user_id))
    artists = []
    for fav in favorites:
        artist = list(Artist.objects.filter(id=fav.artist_id))
        if artist != [] and artist not in artists:
            artists.append(artist)
    return(render(request, 'favorites.html', {'artists': artists}))

def add_like(request):
    song_id = request.POST.get('song_id')
    user_id = request.POST.get('user_id')
    album = request.POST.get('album')
    like = Like(song_id=song_id, user_id=user_id)
    like.save()
    #return(render(request, 'album_page.html', {'album': album}))
    return get_likes(request)

def add_to_favorites(request):
    artist_id = request.POST.get('artist_id')
    user_id = request.POST.get('user_id')
    favorite = Favorite(artist_id=artist_id, user_id=user_id)
    favorite.save()
    return HttpResponseRedirect("../search/")

def add_song(request):
    form = SongForm(request.POST, request.FILES)
    genres = Genre.objects.all()
    if form.is_valid():
        name = request.POST.get('name')
        album = Album.objects.get(id=request.POST.get('album'))
        duration = request.POST.get('duration')
        artist = album.artist
        album_l = list(Album.objects.filter(name=album))
        artist_l = list(Artist.objects.filter(name=artist))
        if album_l != [] and artist_l != []:
            song = Song(name=name, album_id=album_l[0].id, duration=duration, artist_id=artist_l[0].id)
            song.save()
            for g in genres:
                if request.POST.get(g.name) == 'on':
                    sg = SongGenre(song_id=song.id, genre_id=g.id)
                    sg.save()
            return HttpResponseRedirect("../")
        else:
            form = SongForm()
            return render(request, 'add_song.html', {"form": form})
    else:
        form = SongForm()
    return render(request, 'add_song.html', {"form": form, "genres":genres})

def get_playlists(request):
    user_id = request.POST.get('user_id')
    playlists = list(Playlist.objects.filter(user_id=user_id))
    return render(request, 'playlists.html', {'playlists': playlists})

def get_playlist(request):
    playlist_id = request.POST.get('playlist')
    playlist = Playlist.objects.get(id=playlist_id)
    song_pl = list(PlaylistSong.objects.filter(playlist=playlist))
    songs = []
    for s in song_pl:
        songs.append(s.song)
    return render(request, 'playlist.html', {"songs": songs})

def add_songs_playlist(request):
    playlist_id = request.POST.get('playlist')
    playlist = Playlist.objects.get(id=playlist_id)
    songs_in_playlist = list(PlaylistSong.objects.filter(playlist=playlist))
    song_ids = []
    for s in songs_in_playlist:
        song_ids.append(s.song)
    songs = Song.objects.all()
    res = []
    for s in songs:
        if s not in song_ids:
            res.append(s)
    return render(request, 'add_songs_playlist.html', {"songs": res, "playlist_id": playlist_id})

def add_song_to_playlist(request):
    song_id = request.POST.get('song_id')
    playlist_id = request.POST.get('playlist')
    playlist = Playlist.objects.get(id=playlist_id)
    song = Song.objects.get(id=song_id)
    playlist_song = PlaylistSong(song=song, playlist=playlist)
    playlist_song.save()
    return add_songs_playlist(request)

def add_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            user_id = request.POST.get('user_id')
            playlist = Playlist(name=name, user_id=user_id)
            playlist.save()
            return HttpResponseRedirect("../")
    else:
        form = PlaylistForm()
    return render(request, 'add_playlist.html', {'form': form})

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            album_id = request.POST.get('album_id')
            user_id = request.POST.get('user_id')
            title = request.POST.get('title')
            body = request.POST.get('body')
            review = Review(title=title, body=body, user_id=user_id, album_id=album_id)
            review.save()
            return HttpResponseRedirect("../")
    else:   
        form = ReviewForm()
    context = {
        "form" : form,
        "album_id" : request.POST.get('album_id'),
    }
    return render(request, 'add_review.html', context=context)

def delete_album(request):
    album_id = request.POST.get('album_id')
    try:
        album = Album.objects.get(id=album_id)
        album.delete()
        return HttpResponseRedirect("../")
    except:
        return HttpResponseRedirect("../")
    
def delete_artist(request):
    artist_id = request.POST.get('artist_id')
    try:
        artist = Artist.objects.get(id=artist_id)
        artist.delete()
        return HttpResponseRedirect("../")
    except:
        return HttpResponseRedirect("../")
    
def delete_song(request):
    song_id = request.POST.get('song_id')
    try:
        song = Song.objects.get(id=song_id)
        song.delete()
        return HttpResponseRedirect("../")
    except:
        return HttpResponseRedirect("../")

def add_album(request):
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)

        genres = list(Genre.objects.all())
        if form.is_valid():
            for filename, file in request.FILES.items():
                file_id = save_image(request.FILES[filename], 'album cover', filename)
            artist = Artist.objects.get(id=request.POST.get('artist'))
            if artist:
                album = Album(name=request.POST.get('name'), cover_id=file_id, artist=artist, user_id = request.POST.get('user_id'), year=request.POST.get('year'))
                album.save()
                for g in genres:
                    if request.POST.get(g.name) == 'on':
                        ag = AlbumGenre(album=album, genre=g)
                        ag.save()
            return HttpResponseRedirect("../")
    else:
        form = AlbumForm()

    genres = Genre.objects.all()
    artists = Artist.objects.all()
    context = {
        "genres": list(genres),
        "artists": list(artists),
        "form" : form,
    }
    return render(request, 'add_album.html', context=context)
    
def add_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            for filename, file in request.FILES.items():
                file_id = save_image(request.FILES[filename], 'album cover', filename)
            for filename, file in request.FILES.items():
                pass
            artist = Artist(name=request.POST.get('name'), picture_id=file_id)
            artist.save()
            return HttpResponseRedirect("../")
    else:
        form = ArtistForm()
    return render(request, 'add_artist.html', {"form": form})

def get_image(image_id):
    connection = MongoClient("mongodb", 27017)
    database = connection['images']
    collection = database['images']
    fs=gridfs.GridFS(database)
    fs=gridfs.GridFS(database)
    image_data = fs.get(ObjectId(image_id))
    return HttpResponse(image_data, content_type="image/png")

def imgt(request):
    connection = MongoClient("mongodb", 27017)
    database = connection['images']
    collection = database['images']
    fs=gridfs.GridFS(database)
    fs=gridfs.GridFS(database)
    image_data = fs.get(ObjectId('662e5a8c032064d38d5d3791'))
    return HttpResponse(image_data, content_type="image/png")
    # res = []
    # cursor = collection.find({})
    # collection.insert_one({'name': '8079', 'about': 'testing', 'id': 123456})
    # for document in cursor:
    #     res.append(document)
    # #res = collection.find_one({'name': '8079'})
    # return render(request, 'img_test.html', {"image": res})


def save_image(file, about, filename):
    connection = MongoClient("mongodb", 27017)

    database = connection['images']
    collection = database['images']

    fs = gridfs.GridFS(database)
    file_id = fs.put(file,filename=filename)
    data={ "about":about, "file_id":file_id}
    collection.insert_one(data)
    return file_id
