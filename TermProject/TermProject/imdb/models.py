from django.db import models
import cx_Oracle

# Create your models here.

class GENRE:

    @staticmethod
    def read():
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        c = conn.cursor()

        query = "SELECT * FROM GENRE"

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
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.MOVIE values(seq_movie.nextval, :title, :release_date, :rating, :duration, :language, :photo, :description)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()

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

class SHOW:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.SHOW values(seq_show.nextval, :title, :seasons, :episodes, :release_date, :ending_date, :rating, :episode_duration, :language, :photo, :description)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()


class DIRECTOR:

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


class MOVIE_GENRE:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.MOVIE_GENRE values(:mID, :gID)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()


class SHOW_GENRE:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.SHOW_GENRE values(:sID, :gID)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()
