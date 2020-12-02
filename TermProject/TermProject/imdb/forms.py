from django import forms
from .models import *

g = GENRE()

YEARS = [x for x in range(1900, 2021)]
GENRE_CHOICES = g.read()
GENDER = [('Male','Male'), ('Female','Female'), ('Other', 'Other')]
RATE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]

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
    bio = forms.CharField()


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

class AdminUpdateDeathDate(forms.Form):
    name = forms.CharField()
    death_date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))

class AdminUpdateShowSeason(forms.Form):
    title = forms.CharField()
    season = forms.IntegerField()
    episodes = forms.IntegerField(required = False)
    ending_date = forms.DateField(required = False, widget = forms.SelectDateWidget(years = YEARS))

class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices = RATE_CHOICES, widget=forms.Select(), required=True)

class ReviewForm(forms.Form):
    review = forms.CharField()


class SearchByYearForm(forms.Form):
    start_year = forms.ChoiceField(choices = ((str(x), x) for x in range(1900,2021)), widget=forms.Select(), required=True)
    end_year = forms.ChoiceField(choices = ((str(x), x) for x in range(1900,2021)), widget=forms.Select(), required=True)

class DeleteArtistForm(forms.Form):
    aID = forms.IntegerField()

class DeleteDirectorForm(forms.Form):
    dID = forms.IntegerField()

class DeleteMovieForm(forms.Form):
    mID = forms.IntegerField()

class DeleteShowForm(forms.Form):
    sID = forms.IntegerField()