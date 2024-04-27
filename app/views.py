from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from pymongo import MongoClient
import json
import gridfs
import uuid

def success(request):
    return render(request, 'success.html')

@cache_page(60*15)
def index(request):
    return render(request, 'app.html')

@cache_page(60*15)
def search(request):
    genres = Genre.objects.all()
    return render(request, 'search.html', context={"genres": list(genres)})

@cache_page(60*15)
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
        return(render(request, 'artist_page.html', {'artist': a, 'albums': al}))
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
        return(render(request, 'album_page.html', {'album': a, 'data': [a, artist, year, res]}))
    else:
        HttpResponseRedirect("../")
    return(render(request, 'album_page.html', {'album': album}))

def add_album(request):
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)

        genres = list(Genre.objects.all())
        if form.is_valid():
            uid = uuid.uuid4()
            for filename, file in request.FILES.items():
                pass
            artist_name = request.POST.get('artist')
            artist = list(Artist.objects.filter(name=artist_name))
            if artist != []:
                album = Album(name=request.POST.get('name'), cover_id=uid, artist_id=artist[0].id, user_id = request.POST.get('user_id'), year=request.POST.get('year'))
                album.save()
                for g in genres:
                    if request.POST.get(g.name) == 'on':
                        ag = AlbumGenre(album_id=album.id, genre_id=g.id)
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
            uid = uuid.uuid4()
            for filename, file in request.FILES.items():
                pass
            artist = Artist(name=request.POST.get('name'), picture_id=uid)
            artist.save()
            return HttpResponseRedirect("../")
    else:
        form = ArtistForm()
    return render(request, 'add_artist.html', {"form": form})





def save_image(file, name):
    connection = MongoClient("localhost", 27017)

    database = connection['images']
    collection = database['images']

    mydict = {"name": "test"}
    x = collection.insert_one(mydict)
    fs = gridfs.GridFS(database)

    fs.put(file, encoding='utf-8', filename=name)
