from django.shortcuts import get_object_or_404, render
from .forms import *
from django.core.files.storage import FileSystemStorage
import cx_Oracle
from django.http import HttpResponse
from .models import *

# Create your views here.

# def index(request):
#     # dsn_tns = cx_Oracle.makedsn('localhost','1521',service_name='ORCL')
#     # conn = cx_Oracle.connect(user='hr',password='hr',dsn=dsn_tns)
#     # c = conn.cursor()
# #     # print(c)
# #     # print('Success')
# #     # c.execute("SELECT * FROM HR.ARTIST")
# #     # out = ''
# #     # print(c)
# #     # for row in c :
# #     #     out +=str(row) + ' \n '
# #     # conn.close()
# #
# #     # a = GENRE()
# #     # c = {'id':2, 'name': "comedy"}
# #     # a.insert(c)
# #     # res = a.read()
# #     # print(res)
#
#     return HttpResponse(res, content_type="text/plain")

def index(request):
    return render(request, "imdb/index.html")

def movie(request):
    return render(request, "imdb/movies.html")

def login(request):
    return render(request, "imdb/login.html")

def create(request):
    return render(request, "imdb/create_account.html")

def admin_update(request):
    return render(request, "imdb/admin_update_db.html")

def admin_movie_form(request):

    if request.method == "POST" and request.FILES['image']:
        form = MovieForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']
            release_date = form.cleaned_data['release_date']
            rating = form.cleaned_data['rating']
            duration = form.cleaned_data['duration']
            language = form.cleaned_data['language']
            image = request.FILES['image'].read()               #read() CONVERTS IT FROM 'UpoloadedFile' to BYTES
            description = form.cleaned_data['description']

        dict = {'title':title, 'release_date':release_date, 'rating':rating, 'duration':duration, 'language': language, 'photo':image, 'description': description}
        m = MOVIE()
        m.insert(dict)

    form = MovieForm()
    image_bool = True

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool':image_bool})



def admin_show_form(request):

    if request.method == "POST" and request.FILES['image']:
        form = ShowForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            genre = form.cleaned_data['genre']
            seasons = form.cleaned_data['seasons']
            episodes = form.cleaned_data['episodes']
            release_date = form.cleaned_data['release_date']
            ending_date = form.cleaned_data['release_date']
            rating = form.cleaned_data['rating']
            episode_duration = form.cleaned_data['episode_duration']
            language = form.cleaned_data['language']
            image = request.FILES['image'].read()               #read() CONVERTS IT FROM 'UpoloadedFile' to BYTES
            description = form.cleaned_data['description']

        dict = {'title':title, 'seasons':seasons, 'episodes':episodes, 'release_date':release_date, 'ending_date':ending_date, 'rating':rating, 'episode_duration':episode_duration, 'language': language, 'photo':image, 'description':description}
        s = SHOW()
        s.insert(dict)

    form = ShowForm()
    image_bool = True

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_genre_form(request):

    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']

        dict = {'name': name}
        g = GENRE()
        g.insert(dict)

    form = GenreForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form,'image_bool':image_bool})



def admin_artist_form(request):

    if request.method == "POST" and request.FILES['image']:
        form = ArtistForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            gender = form.cleaned_data['gender']
            birth_date = form.cleaned_data['birth_date']
            nationality = form.cleaned_data['nationality']
            birth_place = form.cleaned_data['birth_place']
            death_date = form.cleaned_data['death_date']
            image = request.FILES['image'].read()               #read() CONVERTS IT FROM 'UpoloadedFile' to BYTES

        dict = {'name':name, 'gender':gender, 'birth_date':birth_date, 'nationality':nationality, 'birth_place':birth_place, 'death_date':death_date, 'photo':image}
        a = ARTIST()
        a.insert(dict)

    form = ArtistForm()
    image_bool = True

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})

def admin_director_form(request):

    if request.method == "POST" and request.FILES['image']:
        form = ArtistForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            gender = form.cleaned_data['gender']
            birth_date = form.cleaned_data['birth_date']
            nationality = form.cleaned_data['nationality']
            birth_place = form.cleaned_data['birth_place']
            death_date = form.cleaned_data['death_date']
            image = request.FILES['image'].read()               #read() CONVERTS IT FROM 'UpoloadedFile' to BYTES

        dict = {'name':name, 'gender':gender, 'birth_date':birth_date, 'nationality':nationality, 'birth_place':birth_place, 'death_date':death_date, 'photo':image}
        d = DIRECTOR()
        d.insert(dict)

    form = ArtistForm()
    image_bool = True 

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})
