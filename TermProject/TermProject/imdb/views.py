from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from django.core.files.storage import FileSystemStorage
import cx_Oracle
from django.http import HttpResponse
from .models import *
import base64
import random
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def create_account(request):

    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password2 == password1:

            if User.objects.filter(username=username).exists():                                 ###IF USERNAME IS TAKEN
                messages.info(request, 'Username Taken')
                return redirect("/create_account")

            else:

                dict = {'username': username, 'password': password1}                            ###FOR ORACLE DATABASE
                imdb_user = USERS()
                imdb_user.insert(dict)

                #usID = imdb_user.get_user_id(username)
                #log = LOG_TABLE_USER()
                #log.insert(usID)

                user = User.objects.create_user(username=username, password=password1)          ### FOR DJANGO
                user.save()
                print('user created')
                return redirect('/login')

        else:
            messages.info(request, 'Password not matching')
            return redirect("/create_account")

        #return redirect('/')

    else:
        return render(request, "imdb/create_account.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)

        log = LOG_TABLE_USER()
        imdb_user = USERS()

        if user is not None:
            auth.login(request, user)                                               ###  AUTHENTICATING USER

            usID = imdb_user.get_user_id(username)                                  ### UPDATING LOG TABLE
            log.update_login(usID)

            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('/login')
    else:
        return render(request, "imdb/login.html")


def logout(request):

    imdb_user = USERS()
    log = LOG_TABLE_USER()

    current_user = request.user
    usID = imdb_user.get_user_id(current_user.username)

    #print(current_user.username)

    auth.logout(request)

    log.update_logOut(usID)

    return redirect('/')


def rate(request, choice, id):

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            user = request.user

            imdb_user = USERS()

            usID = imdb_user.get_user_id(user.username)

            if choice == 1:
                movie = MOVIE()
                UM = USER_MOVIE()
                dict = {'rating': rating, 'usID': usID, 'mID': id}

                if UM.record_exists({'usID': usID, 'mID': id}) == 1:
                    # print('yes previous record')
                    UM.update_rating(dict)
                    movie.update_rating(id)

                elif UM.record_exists({'usID': usID, 'mID': id}) == 0:
                    # print('no previous record')
                    UM.insert_rating(dict)
                    movie.update_rating(id)

                else:
                    return

            elif choice == 0:
                show = SHOW()
                US = USER_SHOW()
                dict = {'rating': rating, 'usID': usID, 'sID': id}

                if US.record_exists(dict) == 1:
                    US.update_rating(dict)
                    show.update_rating(id)

                elif US.record_exists(dict) == 0:
                    US.insert_rating(dict)
                    show.update_rating(id)

                else:
                    return

        return redirect('/')

    form = RatingForm()

    return render(request, 'imdb/rate.html', {'form': form})


def review(request, choice, id):

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data['review']
            user = request.user

            imdb_user = USERS()

            usID = imdb_user.get_user_id(user.username)

            if choice == 1:
                UM = USER_MOVIE()
                dict = {'review': review, 'usID': usID, 'mID': id}

                if UM.record_exists({'usID': usID, 'mID': id}) == 1:
                    # print('yes previous record')
                    UM.update_review(dict)

                elif UM.record_exists({'usID': usID, 'mID': id}) == 0:
                    # print('no previous record')
                    UM.insert_review(dict)

                else:
                    return

            elif choice == 0:
                US = USER_SHOW()
                dict = {'review': review, 'usID': usID, 'sID': id}

                if US.record_exists(dict) == 1:
                    US.update_review(dict)

                elif US.record_exists(dict) == 0:
                    US.insert_review(dict)

                else:
                    return

        return redirect('/')

    form = ReviewForm()

    return render(request, 'imdb/rate.html', {'form': form})


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

    dict = {'id': mID, 'choice': 1, 'movie': title, 'encoded': encoded, 'desc': desc}

    conn.close()
    return render(request, "imdb/index.html", dict)



def movie(request, choice, id):
    #m, s = movie_or_show(movie)

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    c = conn.cursor()

    if choice == 1:
        # query = """ SELECT "mID", "Title", TO_CHAR("Release_Date", 'YYYY'), "Rating",
        #             "Duration", "Language", "Photo", "Description"
        #             FROM IMDB.MOVIE
        #             WHERE UPPER("Title") LIKE UPPER(:title) """

        query = """ SELECT "mID", "Title", TO_CHAR("Release_Date", 'YYYY'), "Rating", 
                     "Duration", "Language", "Photo", "Description" 
                     FROM IMDB.MOVIE 
                     WHERE "mID" = (:mID) """

        c.execute(query, {'mID': id})

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

        if rating == 0:
            rating = 'Not Rated'

        query = """ SELECT C."role", A."Name", A."aID", 1
                FROM ARTIST_MOVIE C, ARTIST A
                WHERE C."mID" = (:mID)
                AND C."aID" = A."aID" """                               ### JOIN

        c.execute(query, {'mID': mID})

        cast = c.fetchall()

        query = """ SELECT D."dID", D."Name", 0
                FROM DIRECTOR D, DIRECTOR_MOVIE DM
                WHERE DM."mID" = (:mID)
                AND DM."dID" = D."dID" """                              ### JOIN

        c.execute(query, {'mID': mID})

        director_list = c.fetchall()
        # directors = []
        #
        # for director in director_list:
        #     directors.append(director[0])

        query = """ SELECT G."Name"
                FROM GENRE G, MOVIE_GENRE MG
                WHERE MG."mID" = (:mID)
                AND MG."gID" = G."gID" """                          ### JOIN

        c.execute(query, {'mID': mID})

        genre_list = c.fetchall()

        genres = []

        for genre in genre_list:
            genres.append(genre[0])

        movie_obj = MOVIE()
        reviews = movie_obj.get_reviews(mID)

        dict = {'id': mID, 'title': title, 'release_date': date, 'duration': duration, 'rating': rating, 'language': language,
                'desc': desc, 'photo': encoded, 'cast': cast, 'directors': director_list, 'choice': 1, 'genres': genres, 'reviews': reviews}

    elif choice == 0:
        # query = """     SELECT "sID", "Title", "Season", "Episodes", TO_CHAR("Release_Date", 'YYYY'),
        #                 TO_CHAR("Ending_Date", 'YYYY'), "Rating", "Episode Duration", "Language", "Photo", "Description"
        #                 FROM IMDB.SHOW
        #                 WHERE UPPER("Title") LIKE UPPER(:title) """

        query = """     SELECT "sID", "Title", "Season", "Episodes", TO_CHAR("Release_Date", 'YYYY'), 
                        TO_CHAR("Ending_Date", 'YYYY'), "Rating", "Episode Duration", "Language", "Photo", "Description"
                        FROM IMDB.SHOW
                        WHERE "sID" = (:sID) """

        c.execute(query, {'sID': id})

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

        if rating == 0:
            rating = 'Not Rated'

        query = """ SELECT C."role", A."Name", A."aID", 1
                        FROM ARTIST_SHOW C, ARTIST A
                        WHERE C."sID" = (:sID)
                        AND C."aID" = A."aID" """                               ### JOIN

        c.execute(query, {'sID': sID})

        cast = c.fetchall()

        query = """ SELECT  D."dID", D."Name", 0 
                        FROM DIRECTOR D, DIRECTOR_SHOW DS
                        WHERE DS."sID" = (:sID)
                        AND DS."dID" = D."dID" """                              ### JOIN

        c.execute(query, {'sID': sID})

        director_list = c.fetchall()
        # director_list = zip(director_list)

        # directors = []
        #
        # for director in director_list:
        #     directors.append([director[0], director[1], director[2]])

        query = """ SELECT G."Name"
                    FROM GENRE G, SHOW_GENRE SG
                    WHERE SG."sID" = (:sID)
                    AND SG."gID" = G."gID" """                              ### JOIN

        c.execute(query, {'sID': sID})

        genre_list = c.fetchall()

        genres = []

        for genre in genre_list:
            genres.append(genre[0])

        show_obj = SHOW()
        reviews = show_obj.get_reviews(sID)

        dict = {'id': sID, 'title': title, 'season': season, 'episodes': episodes, 'release_date': release_date,
                'ending_date': ending_date, 'rating': rating, 'duration': duration, 'language': language, 'photo': encoded, 'desc': desc,
                'cast': cast, 'directors': director_list, 'choice': 0, 'genres': genres, 'reviews': reviews}

    conn.close()
    return render(request, "imdb/movies.html", dict)


def artist(request, choice, id):

    #a, d = artist_or_director(actor)
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    c = conn.cursor()

    if choice == 1:
        # query = """ SELECT *
        #         FROM IMDB.ARTIST
        #         WHERE UPPER("Name") LIKE UPPER(:name) """
        query = """ SELECT * 
                    FROM IMDB.ARTIST 
                    WHERE "aID" = (:id) """

        persona = 'Actor'

    elif choice == 0:
        query = """ SELECT * 
                    FROM IMDB.DIRECTOR 
                    WHERE "dID" = (:id) """

        persona = 'Director'

    c.execute(query, {'id': id})

    data = c.fetchall()

    aID = data[0][0]
    name = data[0][1]
    gender = data[0][2]
    birth_date = data[0][3]
    nationality = data[0][4]
    birth_place = data[0][5]
    death_date = data[0][6]
    photo = data[0][7].read()
    bio = data[0][8]

    encoded = base64.b64encode(photo)
    encoded = encoded.decode('utf-8')

    if choice == 1:
        filmography = get_works(id)
    elif choice == 0:
        filmography = get_directions(id)

    dict = {'name': name, 'gender': gender, 'birth_date': birth_date, 'nationality':nationality,
            'birth_place': birth_place, 'death_date': death_date, 'photo': encoded, 'persona': persona, 'filmography': filmography, 'bio':bio}

    conn.close()
    return render(request, "imdb/artist.html", dict)


def search(request):

    if request.method == 'GET':
        name = request.GET.get('search')

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ SELECT "mID", "Title", "Photo", 1 FROM IMDB.MOVIE WHERE UPPER("Title") LIKE UPPER(CONCAT(CONCAT('%',:name), '%'))
                    UNION ALL
                    SELECT "sID", "Title", "Photo", 0 FROM IMDB.SHOW WHERE UPPER("Title") LIKE UPPER(CONCAT(CONCAT('%',:name), '%')) """       #UNION

        cur.execute(query, {'name': name})

        movie_list = cur.fetchall()

        movies = []

        for movie in movie_list:
            # movies.append(movie[0])
            id = movie[0]
            title = movie[1]
            photo = movie[2].read()
            choice = movie[3]

            encoded = base64.b64encode(photo)
            encoded = encoded.decode('utf-8')

            movies.append([id, title, encoded, choice])

        query = """ SELECT "aID", "Name", "Photo", 1 FROM IMDB.ARTIST WHERE UPPER("Name") LIKE UPPER(CONCAT(CONCAT('%',:name), '%'))
                    UNION ALL
                    SELECT "dID", "Name", "Photo", 0 FROM IMDB.DIRECTOR WHERE UPPER("Name") LIKE UPPER(CONCAT(CONCAT('%',:name), '%')) """     ###UNION

        cur.execute(query, {'name': name})

        persons_list = cur.fetchall()

        persons = []

        for person in persons_list:
            # persons.append(person[0])
            id = person[0]
            naam = person[1]
            photo = person[2].read()
            choice = person[3]

            encoded = base64.b64encode(photo)
            encoded = encoded.decode('utf-8')

            persons.append([id, naam, encoded, choice])

        dict = {'movies': movies, 'persons': persons}

        conn.close()

        return render(request, 'imdb/search_list.html', dict)


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

    # movie_list = []

    query = """ SELECT M."Title", M."mID", 1, M."Photo"
                FROM MOVIE M, GENRE G, MOVIE_GENRE MG
                WHERE UPPER(G."Name") LIKE UPPER(:genre)
                AND G."gID" = MG."gID"
                AND M."mID" = MG."mID" 
                UNION ALL
                SELECT S."Title", S."sID", 0, S."Photo"
                FROM SHOW S, GENRE G, SHOW_GENRE SG
                WHERE UPPER(G."Name") LIKE UPPER(:genre)
                AND G."gID" = SG."gID"
                AND S."sID" = SG."sID" """                                  ### JOIN AND UNION

    c.execute(query, {'genre': genre})

    movie_list = c.fetchall()

    movies = []

    for movie in movie_list:
        # movies.append(movie[0])
        title = movie[0]
        id = movie[1]
        photo = movie[3].read()
        choice = movie[2]

        encoded = base64.b64encode(photo)
        encoded = encoded.decode('utf-8')

        movies.append([title, id, choice, encoded])

    dict = {'movie_list': movies}

    return render(request, "imdb/movies_of_this_list.html", dict)


def search_by_year(request):
    if request.method == "POST":
        form = SearchByYearForm(request.POST)
        if form.is_valid():
            start_year = form.cleaned_data['start_year']
            end_year = form.cleaned_data['end_year']


            dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
            conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
            c = conn.cursor()

            movie_list = []

            query = """ SELECT "Title", "mID", 1, "Photo" 
                        FROM IMDB.MOVIE
                        WHERE TO_NUMBER(TO_CHAR("Release_Date", 'YYYY')) BETWEEN (:start_year) AND (:end_year)
                        UNION ALL
                        SELECT "Title", "sID", 0, "Photo"
                        FROM IMDB.SHOW
                        WHERE TO_NUMBER(TO_CHAR("Release_Date", 'YYYY')) BETWEEN (:start_year) AND (:end_year)"""  ### UNION

            c.execute(query, {'start_year': start_year, 'end_year': end_year})

            movie_list = c.fetchall()

            movies = []

            for movie in movie_list:
                # movies.append(movie[0])
                title = movie[0]
                id = movie[1]
                photo = movie[3].read()
                choice = movie[2]

                encoded = base64.b64encode(photo)
                encoded = encoded.decode('utf-8')

                movies.append([title, id, choice, encoded])

            dict = {'movie_list': movies}

            if len(movies) == 0:
                messages.info(request, 'No Movie Or Show Found')
                return redirect('/search_by_year')

            return render(request, "imdb/movies_of_this_list.html", dict)

    form = SearchByYearForm()

    return render(request, "imdb/rate.html", {'form': form})


def top_rated_movies(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    c = conn.cursor()

    movie_list = []

    query = """ SELECT "Title", "Rating", "Photo", "ID", "CHOICE"
                FROM 
                (SELECT "Title", "Rating", "Photo", "mID" AS "ID", 1 AS "CHOICE" FROM MOVIE
                UNION ALL
                SELECT "Title", "Rating", "Photo", "sID" AS "ID", 0 AS "CHOICE" FROM SHOW)
                ORDER BY "Rating" DESC """                                                          ### SUB-QUERY, UNION

    c.execute(query)

    movies = c.fetchall()

    for movie in movies:
        # movies.append(movie[0])
        title = movie[0]
        rating = movie[1]
        photo = movie[2].read()
        id = movie[3]
        choice = movie[4]

        encoded = base64.b64encode(photo)
        encoded = encoded.decode('utf-8')

        movie_list.append([title, rating, encoded, id, choice])

    dict = {'movie_list': movie_list}

    return render(request, "imdb/top_rated_movies.html", dict)



###ADMIN_FUNCTIONS

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
            image = request.FILES['image'].read()                                           # read() CONVERTS IT FROM 'UploadedFile' to BYTES
            description = form.cleaned_data['description']
            genre = form.cleaned_data.get('genre')

        m = MOVIE()
        mg = MOVIE_GENRE()                                                                  # to populate the movie_genre table
        mID = m.get_next_ID()                                                               # get the ID of the movie to be inserted next

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
            image = request.FILES['image'].read()                                          # read() CONVERTS IT FROM 'UploadedFile' to BYTES
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
            bio = form.cleaned_data['bio']
            image = request.FILES['image'].read()                                # read() CONVERTS IT FROM 'UploadedFile' to BYTES


        dict = {'name': name, 'gender': gender, 'birth_date': birth_date, 'nationality': nationality,
                'birth_place': birth_place, 'death_date': death_date, 'photo': image, 'bio': bio}

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
            bio = form.cleaned_data['bio']

        dict = {'name': name, 'gender': gender, 'birth_date': birth_date, 'nationality': nationality,
                'birth_place': birth_place, 'death_date': death_date, 'photo': image, 'bio': bio}
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


def admin_update_artist_death_date(request):
    if request.method == "POST":
        form = AdminUpdateDeathDate(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            death_date = form.cleaned_data['death_date']

        artist = ARTIST()

        aID = artist.get_artist_id(name)

        artist.update_death_date(aID, death_date)

    form = AdminUpdateDeathDate()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_update_director_death_date(request):
    if request.method == "POST":
        form = AdminUpdateDeathDate(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            death_date = form.cleaned_data['death_date']

        director = DIRECTOR()

        dID = director.get_ID(name)

        director.update_death_date(dID, death_date)

    form = AdminUpdateDeathDate()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_update_show_season(request):
    if request.method == "POST":
        form = AdminUpdateShowSeason(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            season = form.cleaned_data['season']
            episodes = form.cleaned_data['episodes']
            ending_date = form.cleaned_data['ending_date']

        show = SHOW()

        sID = show.get_show_id(title)
        show.update_season(sID, season, episodes, ending_date)

    form = AdminUpdateShowSeason()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_delete_movie(request):
    if request.method == "POST":
        form = DeleteMovieForm(request.POST)
        if form.is_valid():
            mID = form.cleaned_data['mID']

        movie = MOVIE()

        movie.delete(mID)

    form = DeleteMovieForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_delete_show(request):
    if request.method == "POST":
        form = DeleteShowForm(request.POST)
        if form.is_valid():
            sID = form.cleaned_data['sID']

        show = SHOW()

        show.delete(sID)

    form = DeleteShowForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_delete_artist(request):
    if request.method == "POST":
        form = DeleteArtistForm(request.POST)
        if form.is_valid():
            aID = form.cleaned_data['aID']

        artist = ARTIST()

        artist.delete(aID)

    form = DeleteArtistForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})


def admin_delete_director(request):
    if request.method == "POST":
        form = DeleteDirectorForm(request.POST)
        if form.is_valid():
            dID = form.cleaned_data['dID']

        director = DIRECTOR()

        director.delete(dID)

    form = DeleteDirectorForm()
    image_bool = False

    return render(request, "imdb/admin_form.html", {'form': form, 'image_bool': image_bool})