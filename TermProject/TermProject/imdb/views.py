from django.shortcuts import get_object_or_404, render
from .forms import *
from django.core.files.storage import FileSystemStorage
import cx_Oracle
from django.http import HttpResponse
from .models import *
import base64
import random


# Create your views here.

def index(request):
    ###SHOWING A RANDOM MOVIE

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    movie = MOVIE()
    mID_rand = random.randint(0, 100)
    mID = mID_rand % movie.get_last_movie_id() + 1

    while movie_exists(mID) == False:
        mID_rand = random.randint(0, 100)
        mID = mID_rand % movie.get_last_movie_id() + 1

    query = """ SELECT "Title", "Photo", "Description" FROM IMDB.MOVIE WHERE "mID" = (:mID) """
    cur.execute(query, {'mID': mID})

    res = cur.fetchall()
    title = res[0][0]
    image = res[0][1]
    desc = res[0][2]

    # Convert the bytes file to base64string. Then decode it to string. Then pass it

    encoded = base64.b64encode(image.read())
    encoded = encoded.decode('utf-8')

    dict = {'movie': title, 'encoded': encoded, 'desc': desc}

    conn.close()
    return render(request, "imdb/index.html", dict)


# def index(request):
#     return render(request, "imdb/index.html")


def movie(request, movie):
    m, s = movie_or_show(movie)

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    c = conn.cursor()

    if m:
        query = """ SELECT "mID", "Title", TO_CHAR("Release_Date", 'YYYY'), "Rating", 
                    "Duration", "Language", "Photo", "Description" 
                    FROM IMDB.MOVIE 
                    WHERE UPPER("Title") LIKE UPPER(:title) """

        c.execute(query, {'title': movie})

        data = c.fetchall()

        mID = data[0][0]
        title = data[0][1]
        date = data[0][2]
        rating = data[0][3]
        duration = data[0][4]
        language = data[0][5]
        photo = data[0][6].read()
        desc = data[0][7]

        encoded = base64.b64encode(photo)
        encoded = encoded.decode('utf-8')

        query = """ SELECT C."role", A."Name" 
                FROM ARTIST_MOVIE C, ARTIST A
                WHERE C."mID" = (:mID)
                AND C."aID" = A."aID" """

        c.execute(query, {'mID': mID})

        cast = c.fetchall()

        query = """ SELECT D."Name" 
                FROM DIRECTOR D, DIRECTOR_MOVIE DM
                WHERE DM."mID" = (:mID)
                AND DM."dID" = D."dID" """

        c.execute(query, {'mID': mID})

        director_list = c.fetchall()
        directors = []

        for director in director_list:
            directors.append(director[0])

        query = """ SELECT G."Name"
                FROM GENRE G, MOVIE_GENRE MG
                WHERE MG."mID" = (:mID)
                AND MG."gID" = G."gID" """

        c.execute(query, {'mID': mID})

        genre_list = c.fetchall()

        genres = []

        for genre in genre_list:
            genres.append(genre[0])

        dict = {'title': title, 'release_date': date, 'duration': duration, 'rating': rating, 'language': language,
                'desc': desc, 'photo': encoded, 'cast': cast, 'directors': director, 'choice': 1, 'genres': genres}

    elif s:
        query = """     SELECT "sID", "Title", "Season", "Episodes", TO_CHAR("Release_Date", 'YYYY'), 
                        TO_CHAR("Ending_Date", 'YYYY'), "Rating", "Episode Duration", "Language", "Photo", "Description"
                        FROM IMDB.SHOW
                        WHERE UPPER("Title") LIKE UPPER(:title) """

        c.execute(query, {'title': movie})

        data = c.fetchall()

        sID = data[0][0]
        title = data[0][1]
        season = data[0][2]
        episodes = data[0][3]
        release_date = data[0][4]
        ending_date = data[0][5]
        rating = data[0][6]
        duration = data[0][7]
        language = data[0][8]
        photo = data[0][9].read()
        desc = data[0][10]

        encoded = base64.b64encode(photo)
        encoded = encoded.decode('utf-8')

        query = """ SELECT C."role", A."Name" 
                        FROM ARTIST_SHOW C, ARTIST A
                        WHERE C."sID" = (:sID)
                        AND C."aID" = A."aID" """

        c.execute(query, {'sID': sID})

        cast = c.fetchall()

        query = """ SELECT D."Name" 
                        FROM DIRECTOR D, DIRECTOR_SHOW DS
                        WHERE DS."sID" = (:sID)
                        AND DS."dID" = D."dID" """

        c.execute(query, {'sID': sID})

        director_list = c.fetchall()
        directors = []

        for director in director_list:
            directors.append(director[0])

        query = """ SELECT G."Name"
                    FROM GENRE G, SHOW_GENRE SG
                    WHERE SG."sID" = (:sID)
                    AND SG."gID" = G."gID" """

        c.execute(query, {'sID': sID})

        genre_list = c.fetchall()

        genres = []

        for genre in genre_list:
            genres.append(genre[0])

        dict = {'title': title, 'season': season, 'episodes': episodes, 'release_date': release_date,
                'ending_date': ending_date, 'rating':rating, 'duration': duration, 'language': language, 'photo': encoded, 'desc': desc,
                'cast': cast, 'directors': directors, 'choice': 0, 'genres': genres}

    conn.close()
    return render(request, "imdb/movies.html", dict)


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
            release_date = form.cleaned_data['release_date']
            rating = form.cleaned_data['rating']
            duration = form.cleaned_data['duration']
            language = form.cleaned_data['language']
            image = request.FILES['image'].read()  # read() CONVERTS IT FROM 'UploadedFile' to BYTES
            description = form.cleaned_data['description']
            genre = form.cleaned_data.get('genre')

        m = MOVIE()
        mg = MOVIE_GENRE()  # to populate the movie_genre table
        mID = m.get_next_ID()  # get the ID of the movie to be inserted next

        dict = {'mID': mID, 'title': title, 'release_date': release_date, 'rating': rating, 'duration': duration,
                'language': language, 'photo': image, 'description': description}

        m.insert(dict)  # insert into movie

        for gID in genre:  # for each genre, populate the table for the same movie
            mg.insert(mID, int(gID))

    form = MovieForm()
    image_bool = True

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_show_form(request):
    if request.method == "POST" and request.FILES['image']:
        form = ShowForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            genre = form.cleaned_data.get('genre')
            seasons = form.cleaned_data['seasons']
            episodes = form.cleaned_data['episodes']
            release_date = form.cleaned_data['release_date']
            ending_date = form.cleaned_data['release_date']
            rating = form.cleaned_data['rating']
            episode_duration = form.cleaned_data['episode_duration']
            language = form.cleaned_data['language']
            image = request.FILES['image'].read()  # read() CONVERTS IT FROM 'UpoloadedFile' to BYTES
            description = form.cleaned_data['description']

        s = SHOW()
        sg = SHOW_GENRE()
        sID = s.get_next_ID()

        dict = {'sID': sID, 'title': title, 'seasons': seasons, 'episodes': episodes, 'release_date': release_date,
                'ending_date': ending_date, 'rating': rating, 'episode_duration': episode_duration,
                'language': language, 'photo': image, 'description': description}

        s.insert(dict)
        # to populate the show_genre table

        for gID in genre:  # for each genre, populate the table for the same movie
            sg.insert(sID, int(gID))

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

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


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
            image = request.FILES['image'].read()  # read() CONVERTS IT FROM 'UpoloadedFile' to BYTES

        dict = {'name': name, 'gender': gender, 'birth_date': birth_date, 'nationality': nationality,
                'birth_place': birth_place, 'death_date': death_date, 'photo': image}
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
            image = request.FILES['image'].read()  # read() CONVERTS IT FROM 'UpoloadedFile' to BYTES

        dict = {'name': name, 'gender': gender, 'birth_date': birth_date, 'nationality': nationality,
                'birth_place': birth_place, 'death_date': death_date, 'photo': image}
        d = DIRECTOR()
        d.insert(dict)

    form = ArtistForm()
    image_bool = True

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_artist_movie_form(request):
    if request.method == "POST":
        form = ArtistMovieForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['movie']
            artist_name = form.cleaned_data['artist']
            role = form.cleaned_data['role']

        movie = MOVIE()
        artist = ARTIST()
        mID = movie.get_movie_id(movie_title)
        aID = artist.get_artist_id(artist_name)

        dict = {'role': role, 'aID': aID, 'mID': mID}

        artist_movie = ARTIST_MOVIE()
        artist_movie.insert(dict)

    form = ArtistMovieForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_artist_show_form(request):
    if request.method == "POST":
        form = ArtistShowForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['show']
            artist_name = form.cleaned_data['artist']
            role = form.cleaned_data['role']

        show = SHOW()
        artist = ARTIST()
        sID = show.get_show_id(movie_title)
        aID = artist.get_artist_id(artist_name)

        dict = {'role': role, 'aID': aID, 'sID': sID}

        artist_show = ARTIST_SHOW()
        artist_show.insert(dict)

    form = ArtistShowForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def browse_by_genre(request):
    g = GENRE()
    genres = g.read()

    genre_list = []

    for genre in genres:
        genre_list.append(genre[1])

    dict = {'genre_list': genre_list}

    return render(request, "imdb/browse_movie_by_genre.html", dict)


def movies_of_genre(request, genre):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    c = conn.cursor()

    movie_list = []

    query = """ SELECT M."Title"
                FROM MOVIE M, GENRE G, MOVIE_GENRE MG
                WHERE UPPER(G."Name") LIKE UPPER(:genre)
                AND G."gID" = MG."gID"
                AND M."mID" = MG."mID" 
                UNION
                SELECT S."Title"
                FROM SHOW S, GENRE G, SHOW_GENRE SG
                WHERE UPPER(G."Name") LIKE UPPER(:genre)
                AND G."gID" = SG."gID"
                AND S."sID" = SG."sID" """

    c.execute(query, {'genre': genre})

    movies = c.fetchall()

    for movie in movies:
        movie_list.append(movie[0])

    dict = {'movie_list': movie_list}

    return render(request, "imdb/movies_of_this_genre.html", dict)


def artist(request, actor):

    a, d = artist_or_director(actor)

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    c = conn.cursor()

    if a:
        query = """ SELECT * 
                FROM IMDB.ARTIST 
                WHERE UPPER("Name") LIKE UPPER(:name) """

        persona = 'Actor'

    elif d:
        query = """ SELECT * 
                    FROM IMDB.DIRECTOR 
                    WHERE UPPER("Name") LIKE UPPER(:name) """

        persona = 'Director'

    c.execute(query, {'name': actor})

    data = c.fetchall()

    aID = data[0][0]
    name = data[0][1]
    gender = data[0][2]
    birth_date = data[0][3]
    nationality = data[0][4]
    birth_place = data[0][5]
    death_date = data[0][6]
    photo = data[0][7].read()

    encoded = base64.b64encode(photo)
    encoded = encoded.decode('utf-8')

    if a:
        filmography = get_works(name)
    elif d:
        filmography = get_directions(name)

    dict = {'name':name, 'gender':gender, 'birth_date':birth_date, 'nationality':nationality,
            'birth_place':birth_place, 'death_date':death_date, 'photo':encoded, 'persona': persona, 'filmography': filmography}

    conn.close()
    return render(request, "imdb/artist.html", dict)

def admin_director_movie_form(request):
    if request.method == "POST":
        form = DirectorMovieForm(request.POST)
        if form.is_valid():
            movie_title = form.cleaned_data['movie']
            director_name = form.cleaned_data['director']

        movie = MOVIE()
        director = DIRECTOR()
        mID = movie.get_movie_id(movie_title)
        dID = director.get_ID(director_name)

        dict = {'dID': dID, 'mID': mID}

        director_movie = DIRECTOR_MOVIE()
        director_movie.insert(dict)

    form = DirectorMovieForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})

def admin_director_show_form(request):
    if request.method == "POST":
        form = DirectorShowForm(request.POST)
        if form.is_valid():
            show_title = form.cleaned_data['show']
            director_name = form.cleaned_data['director']

        show = SHOW()
        director = DIRECTOR()

        sID = show.get_show_id(show_title)
        dID = director.get_ID(director_name)

        dict = {'dID': dID, 'sID': sID}

        director_show = DIRECTOR_SHOW()
        director_show.insert(dict)

    form = DirectorShowForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def search(request):

    if request.method == 'GET':
        name = request.GET.get('search')

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ SELECT "Title" FROM IMDB.MOVIE WHERE UPPER("Title") LIKE UPPER(CONCAT(CONCAT('%',:name), '%'))
                    UNION
                    SELECT "Title" FROM IMDB.SHOW WHERE UPPER("Title") LIKE UPPER(CONCAT(CONCAT('%',:name), '%')) """

        cur.execute(query, {'name': name})

        movie_list = cur.fetchall()

        movies = []

        for movie in movie_list:
            movies.append(movie[0])

        query = """ SELECT "Name" FROM IMDB.ARTIST WHERE UPPER("Name") LIKE UPPER(CONCAT(CONCAT('%',:name), '%'))
                    UNION
                    SELECT "Name" FROM IMDB.DIRECTOR WHERE UPPER("Name") LIKE UPPER(CONCAT(CONCAT('%',:name), '%')) """

        cur.execute(query, {'name': name})

        persons_list = cur.fetchall()

        persons = []

        for person in persons_list:
            persons.append(person[0])

        dict = {'movies': movies, 'persons': persons}

        conn.close()

        return render(request, 'imdb/search_list.html', dict)