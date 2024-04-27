from django.conf import settings
from django.db import models


class Image(models.Model):
    img = models.ImageField()

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.role


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role_id = models.IntegerField()

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    user_id = models.IntegerField()
    cover_id = models.CharField(max_length=100)
    artist_id = models.IntegerField()
    year = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    album_id = models.IntegerField()
    duration = models.IntegerField()
    artist_id = models.IntegerField()

    def __str__(self):
        return self.name


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'
        

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    album_id = models.IntegerField()
    rating = models.IntegerField()
    created_at = models.DateField()


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    user_id = models.IntegerField()

    def __str__(self):
        return self.name



class CollectionAlbum(models.Model):
    id = models.AutoField(primary_key=True)
    collection_id = models.IntegerField()
    album_id = models.IntegerField()


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    user_id = models.IntegerField()

    def __str__(self):
        return self.name



class PlaylistSong(models.Model):
    id = models.AutoField(primary_key=True)
    playlist_id = models.IntegerField()
    song_id = models.IntegerField()


class AlbumGenre(models.Model):
    id = models.AutoField(primary_key=True)
    album_id = models.IntegerField()
    genre_id = models.IntegerField()

    def __str__(self):
        return f'{Album.objects.get(id=self.album_id).name} -> {Genre.objects.get(id=self.genre_id).name}'

class SongGenre(models.Model):
    id = models.AutoField(primary_key=True)
    song_id = models.IntegerField()
    genre_id = models.IntegerField()


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    body = models.TextField()
    user_id = models.IntegerField()
    album_id = models.IntegerField()


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    picture_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    artist_id = models.IntegerField()