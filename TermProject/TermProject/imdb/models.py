from django.db import models
import cx_Oracle

# Create your models here.

class GENRE:

    @staticmethod
    def read():
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        c = conn.cursor()

        query = "SELECT * FROM IMDB.GENRE"

        c.execute(query)

        res = c.fetchall()
        conn.close()
        return res

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.GENRE VALUES(seq_genre.nextval, :name)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()

class MOVIE:

    @staticmethod
    def get_next_ID():
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "SELECT seq_movie.nextval from DUAL"

        cur.execute(query)

        mID = cur.fetchall()

        conn.close()

        return mID[0][0]

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.MOVIE values(:mID, :title, :release_date, :rating, :duration, :language, :photo, :description)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def get_movie_id(movie_title):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """SELECT "mID" FROM IMDB.MOVIE WHERE UPPER("Title") LIKE UPPER(:title)"""

        dict = {'title': movie_title}

        cur.execute(query, dict)

        mID = cur.fetchall()

        conn.commit()
        conn.close()

        return mID[0][0]

    @staticmethod
    def get_last_movie_id():
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ SELECT "mID" FROM 
                    (SELECT * FROM MOVIE 
                    ORDER BY "mID" DESC) 
                    WHERE ROWNUM = 1 """

        cur.execute(query)

        mID = cur.fetchall()

        conn.commit()
        conn.close()

        return mID[0][0]

    # @staticmethod
    # def get_movie(title):
    #     dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    #     conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    #     c = conn.cursor()
    #
    #     query = """ SELECT "Title","Release_Date","Rating","Duration","Language","Photo","Description"
    #                 FROM IMDB.MOVIE
    #                 WHERE UPPER("Title") LIKE UPPER(:title) """
    #
    #     c.execute(query, {'title': title})
    #
    #     res = c.fetchall()
    #
    #     conn.close()
    #     return res

class ARTIST:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.ARTIST values(seq_artist.nextval, :name, :gender, :birth_date, :nationality, :birth_place, :death_date, :photo)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def get_artist_id(artist_name):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """SELECT "aID" FROM IMDB.ARTIST WHERE UPPER("Name") LIKE UPPER(:name)"""

        dict = {'name': artist_name}

        cur.execute(query, dict)

        aID = cur.fetchall()

        conn.commit()
        conn.close()

        return aID[0][0]


class SHOW:

    @staticmethod
    def get_next_ID():
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "SELECT seq_show.nextval from DUAL"

        cur.execute(query)

        sID = cur.fetchall()

        conn.close()

        return sID[0][0]

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.SHOW values(:sid, :title, :seasons, :episodes, :release_date, :ending_date, :rating, :episode_duration, :language, :photo, :description)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def get_show_id(show_title):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """SELECT "sID" FROM IMDB.SHOW WHERE UPPER("Title") LIKE UPPER(:title)"""

        dict = {'title': show_title}

        cur.execute(query, dict)

        sID = cur.fetchall()

        conn.commit()
        conn.close()

        return sID[0][0]


class DIRECTOR:

    @staticmethod
    def get_ID(director):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """SELECT "dID" FROM IMDB.DIRECTOR WHERE UPPER("Name") LIKE UPPER(:director)"""
        cur.execute(query, {'director':director})

        dID = cur.fetchall()

        conn.close()

        return dID[0][0]


    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.DIRECTOR values(seq_director.nextval, :name, :gender, :birth_date, :nationality, :birth_place, :death_date, :photo)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()


class ARTIST_MOVIE:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.ARTIST_MOVIE values(:role, :aID, :mID)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()
    #
    # @staticmethod
    # def get_movies(artist_name):
    #     dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    #     conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    #     cur = conn.cursor()
    #
    #     query = """ SELECT M."Title", AM."role"
    #                 FROM MOVIE M, ARTIST A, ARTIST_MOVIE AM
    #                 WHERE UPPER(A."Name") LIKE UPPER(:artist_name)
    #                 AND A."aID" = AM."aID"
    #                 AND M."mID" = AM."mID" """
    #
    #     dict = {'artist_name': artist_name}
    #
    #     cur.execute(query, dict)
    #
    #     movies = []
    #
    #     movie_list = cur.fetchall()
    #
    #     for movie in movie_list:
    #         movies.append(movie[0])
    #
    #     conn.commit()
    #     conn.close()
    #
    #     return movies

class ARTIST_SHOW:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.ARTIST_SHOW values(:role, :aID, :sID)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    # @staticmethod
    # def get_shows(artist_name):
    #     dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    #     conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    #     cur = conn.cursor()
    #
    #     query = """ SELECT S."Title", ASW."role"
    #                     FROM SHOW S, ARTIST A, ARTIST_SHOW ASW
    #                     WHERE UPPER(A."Name") LIKE UPPER(:artist_name)
    #                     AND A."aID" = ASW."aID"
    #                     AND S."sID" = ASW."sID" """
    #
    #     dict = {'artist_name': artist_name}
    #
    #     cur.execute(query, dict)
    #
    #     shows = []
    #
    #     show_list = cur.fetchall()
    #
    #     for show in show_list:
    #         shows.append(show[0])
    #
    #     conn.commit()
    #     conn.close()
    #
    #     return shows


class MOVIE_GENRE:

    @staticmethod
    def insert(mID, gID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """INSERT INTO IMDB.MOVIE_GENRE values(:mID, :gID)"""

        cur.execute(query, {'mID':mID, 'gID':gID})
        conn.commit()
        conn.close()


class SHOW_GENRE:

    @staticmethod
    def insert(sID, gID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.SHOW_GENRE values(:sID, :gID)"

        cur.execute(query, {'sID':sID, 'gID':gID})
        conn.commit()
        conn.close()


class DIRECTOR_MOVIE:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.DIRECTOR_MOVIE values(:dID, :mID)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()


class DIRECTOR_SHOW:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.DIRECTOR_SHOW values(:dID, :sID)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()


#functions
def movie_or_show(title):

    movie = False
    show = False

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    query = """SELECT "mID" FROM IMDB.MOVIE WHERE UPPER("Title") LIKE UPPER(:title)"""

    dict = {'title': title}

    cur.execute(query, dict)

    mID = cur.fetchall()

    if len(mID) != 0:
        movie = True

    else:
        query = """SELECT "sID" FROM IMDB.SHOW WHERE UPPER("Title") LIKE UPPER(:title)"""

        dict = {'title': title}

        cur.execute(query, dict)

        sID = cur.fetchall()

        if len(sID) != 0:
            show = True

    return movie, show


def artist_or_director(name):

    artist = False
    director = False

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    query = """SELECT "aID" FROM IMDB.Artist WHERE UPPER("Name") LIKE UPPER(:name)"""

    dict = {'name': name}

    cur.execute(query, dict)

    aID = cur.fetchall()

    if len(aID) != 0:
        artist = True

    else:
        query = """SELECT "dID" FROM IMDB.DIRECTOR WHERE UPPER("Name") LIKE UPPER(:name)"""

        dict = {'name': name}

        cur.execute(query, dict)

        dID = cur.fetchall()

        if len(dID) != 0:
            director = True

    return artist, director


def get_works(artist_name):

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    query = """ SELECT M."Title", AM."role"
                FROM MOVIE M, ARTIST A, ARTIST_MOVIE AM
                WHERE UPPER(A."Name") LIKE UPPER(:artist_name)
                AND A."aID" = AM."aID"
                AND M."mID" = AM."mID" 
                UNION
                SELECT S."Title", ASW."role"
                FROM SHOW S, ARTIST A, ARTIST_SHOW ASW
                WHERE UPPER(A."Name") LIKE UPPER(:artist_name)
                AND A."aID" = ASW."aID"
                AND S."sID" = ASW."sID" """

    cur.execute(query, {'artist_name': artist_name})

    works = cur.fetchall()

    return works

def get_directions(director_name):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    query = """ SELECT S."Title"
                FROM SHOW S, DIRECTOR D, DIRECTOR_SHOW DS
                WHERE UPPER(D."Name") LIKE UPPER(:director_name)
                AND D."dID" = DS."dID"
                AND S."sID" = DS."sID"
                UNION
                SELECT M."Title"
                FROM MOVIE M, DIRECTOR D, DIRECTOR_MOVIE DM
                WHERE UPPER(D."Name") LIKE UPPER(:director_name)
                AND D."dID" = DM."dID"
                AND M."mID" = DM."mID" """

    cur.execute(query, {':director_name': director_name})

    movie_list = cur.fetchall()

    movies = []

    for movie in movie_list:
        movies.append(movie[0])

    return movies

def movie_exists(mID):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    query = """ SELECT "mID" FROM 
                    IMDB.MOVIE WHERE "mID" = (:mID) """

    cur.execute(query, {'mID': mID})

    mID = cur.fetchall()

    conn.close()

    if len(mID) == 0:
        return False

    else:
        return True
