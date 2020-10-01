from django import forms

YEARS = [x for x in range(1900, 2021)]

class MovieForm(forms.Form):
    title = forms.CharField()
    genre = forms.ChoiceField(choices = [('Horror', "Horror"), ("Thriller", "Thriller")])
    release_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
    rating = forms.IntegerField(max_value=5, min_value=0)
    duration = forms.IntegerField()
    language = forms.CharField()
    description = forms.CharField()


class ShowForm(forms.Form):
    title = forms.CharField()
    genre = forms.ChoiceField(choices = [('Horror', "Horror"), ("Thriller", "Thriller")])
    seasons = forms.IntegerField()
    episodes = forms.IntegerField()
    release_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
    ending_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
    rating = forms.IntegerField(max_value=5, min_value=0)
    episode_duration = forms.IntegerField()
    language = forms.CharField()
    description = forms.CharField()


class GenreForm(forms.Form):
    name = forms.CharField()

class ArtistForm(forms.Form):
    name = forms.CharField()
    gender = forms.CharField()
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
    nationality = forms.CharField()
    birth_place = forms.CharField()
    death_date = forms.DateField(widget=forms.SelectDateWidget(years = YEARS))
