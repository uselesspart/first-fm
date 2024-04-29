from django import forms


class ArtistForm(forms.Form):
    name = forms.CharField(max_length=100)
    file = forms.FileField()

class AlbumForm(forms.Form):
    name = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=100)
    year = forms.IntegerField()
    file = forms.FileField()

class SongForm(forms.Form):
    name = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=100)
    duration = forms.IntegerField()
    album = forms.CharField(max_length=100)

class ReviewForm(forms.Form):
    title = forms.CharField(max_length=100)