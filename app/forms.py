from django import forms
from .models import *

class ArtistForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    file = forms.FileField(label='Изображение')

class AlbumForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(), empty_label='...', label='Исполнитель')
    year = forms.IntegerField(label='Год')
    file = forms.FileField(label='Изображение')

class SongForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')
    duration = forms.IntegerField(label='Длительность(секунды)')
    album = forms.ModelChoiceField(queryset=Album.objects.all(), empty_label='...', label='Альбом')

class ReviewForm(forms.Form):
    title = forms.CharField(max_length=100, label='Заголовок')

class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название')