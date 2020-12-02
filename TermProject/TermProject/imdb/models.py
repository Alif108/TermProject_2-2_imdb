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
                    WHERE ROWNUM = 1 """                        #   SUB-QUERY

        cur.execute(query)

        mID = cur.fetchall()

        conn.commit()
        conn.close()

        return mID[0][0]

    @staticmethod
    def update_rating(mID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        # query = """ SELECT ROUND(AVG("rating"), 1)
        #             FROM USER_MOVIE
        #             GROUP BY "mID"
        #             HAVING "mID" = (:mID) """
        #
        # cur.execute(query, {'mID': mID})
        #
        # rating = cur.fetchall()
        # rating = rating[0][0]

        query = """ UPDATE IMDB.MOVIE
                    SET "Rating" = (SELECT ROUND(AVG("rating"), 1)                                              
                     FROM USER_MOVIE
                     GROUP BY "mID"
                     HAVING "mID" = (:mID))
                    WHERE "mID" = (:mID) """                                                        ###SUB-QUERY, AGGREGATE FUNCTION

        dict = {'mID': mID}

        cur.execute(query, dict)

        conn.commit()
        conn.close()


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

    @staticmethod
    def get_reviews(mID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ SELECT U."User_Name", UM."review" FROM USERS U, USER_MOVIE UM
            WHERE UM."mID" = (:mID) 
            AND U."usID" = UM."usID"
            AND UM."review" IS NOT NULL """                                                            ###JOIN

        cur.execute(query, {'mID': mID})

        res = cur.fetchall()

        conn.close()

        return res

    @staticmethod
    def delete(mID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ DELETE FROM IMDB.MOVIE
                    WHERE "mID" = (:mID)    """

        cur.execute(query, {'mID': mID})
        conn.commit()

        conn.close()



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

        query = "INSERT INTO IMDB.SHOW values(:sid, :title, :seasons, :episodes, :release_date, " \
                ":ending_date, :rating, :episode_duration, :language, :photo, :description)"

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

    @staticmethod
    def update_season(sID, season, episodes, ending_date):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.SHOW
                    SET "Season" = (:season), "Episodes" = (:episodes), "Ending_Date" = (:ending_date)
                    WHERE "sID" = (:sID)"""

        dict = {'season': season, 'episodes': episodes, 'ending_date': ending_date, 'sID': sID}
        cur.execute(query, dict)

        conn.commit()
        conn.close()

    @staticmethod
    def update_rating(sID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        # query = """ SELECT ROUND(AVG("rating"), 1)
        #                 FROM USER_SHOW
        #                 GROUP BY "sID"
        #                 HAVING "sID"= (:sID) """
        #
        # cur.execute(query, {'sID': sID})
        #
        # rating = cur.fetchall()
        # rating = rating[0][0]

        query = """ UPDATE IMDB.SHOW
                    SET "Rating" = (SELECT ROUND(AVG("rating"), 1)                                             
                    FROM USER_SHOW
                    GROUP BY "sID"
                    HAVING "sID"= (:sID))
                    WHERE "sID" = (:sID) """                                              ### SUB-QUERY, AGGREGATE FUNCTION

        dict = {'sID': sID}

        cur.execute(query, dict)

        conn.commit()
        conn.close()

    @staticmethod
    def get_reviews(sID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ SELECT U."User_Name", US."review" FROM USERS U, USER_SHOW US
                WHERE US."sID" = (:sID) 
                AND U."usID" = US."usID"
                AND US."review" IS NOT NULL """                                        ###JOIN

        cur.execute(query, {'sID': sID})

        res = cur.fetchall()

        conn.close()

        return res

    @staticmethod
    def delete(sID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ DELETE FROM IMDB.SHOW
                        WHERE "sID" = (:sID)    """

        cur.execute(query, {'sID': sID})
        conn.commit()

        conn.close()



class ARTIST:

    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.ARTIST values(seq_artist.nextval, :name, :gender, :birth_date, :nationality, :birth_place, :death_date, :photo, :bio)"

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

    @staticmethod
    def update_death_date(aID, death_date):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.ARTIST
                    SET "Death_Date" = (:death_date)
                    WHERE "aID" = (:aID) """

        dict = {'death_date': death_date, 'aID': aID}

        cur.execute(query, dict)

        conn.commit()
        conn.close()

    @staticmethod
    def delete(aID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ DELETE FROM IMDB.ARTIST
                            WHERE "aID" = (:aID)    """

        cur.execute(query, {'aID': aID})
        conn.commit()

        conn.close()



class DIRECTOR:

    @staticmethod
    def get_ID(director):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """SELECT "dID" FROM IMDB.DIRECTOR WHERE UPPER("Name") LIKE UPPER(:director)"""
        cur.execute(query, {'director': director})

        dID = cur.fetchall()

        conn.close()

        return dID[0][0]

    @staticmethod
    def update_death_date(dID, death_date):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.DIRECTOR
                        SET "Death_Date" = (:death_date)
                        WHERE "dID" = (:dID) """

        dict = {'death_date': death_date, 'dID': dID}

        cur.execute(query, dict)

        conn.commit()
        conn.close()


    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = "INSERT INTO IMDB.DIRECTOR values(seq_director.nextval, :name, :gender, " \
                ":birth_date, :nationality, :birth_place, :death_date, :photo, :bio)"

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def delete(dID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ DELETE FROM IMDB.DIRECTOR
                            WHERE "dID" = (:dID)    """

        cur.execute(query, {'dID': dID})
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

        query = """ INSERT INTO IMDB.MOVIE_GENRE values(:mID, :gID) """

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


class USERS:
    @staticmethod
    def insert(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ INSERT INTO IMDB.USERS values(seq_users.nextval, :username, :password) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_id(username):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ SELECT "usID" FROM IMDB.USERS WHERE "User_Name" LIKE (:name) """

        dict = {'name': username}

        cur.execute(query, dict)

        usID = cur.fetchall()
        conn.close()

        return usID[0][0]


class USER_MOVIE:

    @staticmethod
    def record_exists(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        usID = dict["usID"]
        mID = dict["mID"]

        returnVal = cur.var(int)

        cur.callproc("IMDB.USER_MOVIE_EXISTS", [usID, mID, returnVal])  ###PL/SQL PROCEDURE

        conn.close()

        return returnVal.getvalue()

    @staticmethod
    def insert_rating(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ INSERT INTO IMDB.USER_MOVIE values(:rating, :usID, :mID, NULL, SYSDATE, NULL) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def update_rating(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.USER_MOVIE
                            SET "rating" = (:rating),
                                "rating_log" = SYSDATE
                            WHERE "usID" = (:usID) AND "mID" = (:mID) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def insert_review(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ INSERT INTO IMDB.USER_MOVIE values(NULL, :usID, :mID, :review, NULL, SYSDATE) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def update_review(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.USER_MOVIE
                                    SET "review" = (:review),
                                        "review_log" = SYSDATE
                                    WHERE "usID" = (:usID) AND "mID" = (:mID) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()


class USER_SHOW:

    @staticmethod
    def record_exists(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        usID = dict["usID"]
        sID = dict["sID"]

        returnVal = cur.var(int)

        cur.callproc("IMDB.USER_SHOW_EXISTS", [usID, sID, returnVal])  ###PL/SQL PROCEDURE

        conn.close()

        return returnVal.getvalue()

    @staticmethod
    def insert_rating(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ INSERT INTO IMDB.USER_SHOW values(:rating, :usID, :sID, NULL, SYSDATE, NULL) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def update_rating(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.USER_SHOW
                            SET "rating" = (:rating),
                                "rating_log" = SYSDATE
                            WHERE "usID" = (:usID) AND "sID" = (:sID) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def insert_review(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ INSERT INTO IMDB.USER_SHOW values(NULL, :usID, :sID, :review, NULL, SYSDATE) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()

    @staticmethod
    def update_review(dict):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.USER_SHOW
                                SET "review" = (:review),
                                    "review_log" = SYSDATE
                                WHERE "usID" = (:usID) AND "sID" = (:sID) """

        cur.execute(query, dict)
        conn.commit()
        conn.close()


class LOG_TABLE_USER:
    @staticmethod
    def insert(usID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ INSERT INTO IMDB.LOG_TABLE_USER values(:usID, NULL, NULL) """

        cur.execute(query, {'usID': usID})
        conn.commit()
        conn.close()

    @staticmethod
    def update_login(usID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.LOG_TABLE_USER
                            SET "LogIn" = SYSDATE
                            WHERE "usID" = (:usID) """

        cur.execute(query, {'usID': usID})
        conn.commit()
        conn.close()

    @staticmethod
    def update_logOut(usID):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
        cur = conn.cursor()

        query = """ UPDATE IMDB.LOG_TABLE_USER
                                SET "LogOut" = SYSDATE
                                WHERE "usID" = (:usID) """

        cur.execute(query, {'usID': usID})
        conn.commit()
        conn.close()



####    global_functions

def movie_or_show(title):

    movie = False
    show = False

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    # query = """ SELECT "mID" FROM IMDB.MOVIE WHERE UPPER("Title") LIKE UPPER(:title) """
    #
    # dict = {'title': title}
    #
    # cur.execute(query, dict)
    #
    # mID = cur.fetchall()
    #
    # if len(mID) != 0:
    #     movie = True
    #
    # else:
    #     query = """SELECT "sID" FROM IMDB.SHOW WHERE UPPER("Title") LIKE UPPER(:title)"""
    #
    #     dict = {'title': title}
    #
    #     cur.execute(query, dict)
    #
    #     sID = cur.fetchall()
    #
    #     if len(sID) != 0:
    #         show = True

    flag = cur.callfunc("IMDB.MOVIE_OR_SHOW", int, [title])                 ###PL/SQL FUNCTION

    conn.close()

    if flag == 1:
        movie = True
    elif flag == 0:
        show = True
    else:
        pass

    return movie, show


def artist_or_director(name):

    artist = False
    director = False

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    cur = conn.cursor()

    # query = """SELECT "aID" FROM IMDB.Artist WHERE UPPER("Name") LIKE UPPER(:name)"""
    #
    # dict = {'name': name}
    #
    # cur.execute(query, dict)
    #
    # aID = cur.fetchall()
    #
    # if len(aID) != 0:
    #     artist = True
    #
    # else:
    #     query = """SELECT "dID" FROM IMDB.DIRECTOR WHERE UPPER("Name") LIKE UPPER(:name)"""
    #
    #     dict = {'name': name}
    #
    #     cur.execute(query, dict)
    #
    #     dID = cur.fetchall()
    #
    #     if len(dID) != 0:
    #         director = True

    flag = cur.callfunc("IMDB.ARTIST_OR_DIRECTOR", int, [name])                     ###PL/SQL FUNCTION

    conn.close()

    if flag == 1:
        artist = True
    elif flag == 0:
        director = True
    else:
        pass

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
                AND S."sID" = ASW."sID" """                                     ### JOIN STATEMENT

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
                AND M."mID" = DM."mID" """                                          ### JOIN STATEMENT

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

    # query = """ SELECT "mID" FROM
    #                 IMDB.MOVIE WHERE "mID" = (:mID) """
    #
    # cur.execute(query, {'mID': mID})
    #
    # mID = cur.fetchall()

    returnVal = cur.callfunc("IMDB.MOVIE_EXISTS", int, [mID])                    ###PL/SQL FUNCTION

    conn.close()

    if returnVal == 0:
        return False

    else:
        return True