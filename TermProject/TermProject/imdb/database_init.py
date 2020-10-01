from imdb import IMDb
import cx_Oracle


# create an instance of the IMDb class
ia = IMDb()

def unique(list):                                           #returns unique values of a list
    unique_list = []

    for x in list:
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


def init_genre():

    # genre_list = []
    #
    # for i in range(5):
    #     id = i+1;
    #     movie = ia.get_movie(str(id))
    #
    #     for g in movie['genre']:
    #         genre_list.append(g)
    #
    # dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    # conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
    # c = conn.cursor()
    #
    # genre_unique = unique(genre_list)
    #
    # for genre in genre_unique:
    #     dict = {'name': genre}
    #     query = "INSERT INTO IMDB.GENRE VALUES(gi.nextval, :name)"
    #     c.execute(query, dict)
    #
    # conn.commit()
    # query = "SELECT * FROM IMDB.GENRE"
    #
    # c.execute(query)
    #
    # res = c.fetchall()
    # print(res)
    # conn.close()

    movie = ia.get_movie('10')

    # for i in movie.keys():
    #     print(i)

    print(movie['directors'])


init_genre()

