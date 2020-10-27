from django import forms
from .models import *

g = GENRE()

YEARS = [x for x in range(1900, 2021)]
GENRE_CHOICES = g.read()
GENDER = [('male','Male'), ('female','Female'), ('other', 'Other')]

class MovieForm(forms.Form):
    title = forms.CharField()
    release_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
    rating = forms.IntegerField(max_value=5, min_value=0)
    duration = forms.IntegerField()
    language = forms.CharField()
    description = forms.CharField(widget = forms.Textarea)
    genre = forms.MultipleChoiceField(choices=GENRE_CHOICES)


class ShowForm(forms.Form):
    title = forms.CharField()
    genre = forms.MultipleChoiceField(choices = GENRE_CHOICES)
    seasons = forms.IntegerField()
    episodes = forms.IntegerField()
    release_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
    ending_date = forms.DateField(required = False, widget = forms.SelectDateWidget(years = YEARS))
    rating = forms.IntegerField(max_value=5, min_value=0)
    episode_duration = forms.IntegerField()
    language = forms.CharField()
    description = forms.CharField()


class GenreForm(forms.Form):
    name = forms.CharField()


class ArtistForm(forms.Form):
    name = forms.CharField()
    gender = forms.CharField(widget=forms.Select(choices = GENDER))
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
    nationality = forms.CharField()
    birth_place = forms.CharField()
    death_date = forms.DateField(required = False, widget=forms.SelectDateWidget(years = YEARS))


class ArtistMovieForm(forms.Form):
    movie = forms.CharField()
    artist = forms.CharField()
    role = forms.CharField()


class ArtistShowForm(forms.Form):
    show = forms.CharField()
    artist = forms.CharField()
    role = forms.CharField()


class DirectorMovieForm(forms.Form):
    movie = forms.CharField()
    director = forms.CharField()


class DirectorShowForm(forms.Form):
    show = forms.CharField()
    director = forms.CharField()