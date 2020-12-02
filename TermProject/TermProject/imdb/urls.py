from django.urls import path

from . import views

app_name = 'imdb'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<str:movie>', views.movie, name='movie'),
    path('rate/<int:choice>/<int:id>', views.rate, name='rate'),
    path('review/<int:choice>/<int:id>', views.review, name='review'),
    path('artist/<str:actor>', views.artist, name='artist'),
    path('artist/<str:director>', views.artist, name='director'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create_account/', views.create_account, name="create_account"),
    path('search_results/', views.search, name="search"),
    path('admin_update/', views.admin_update, name="admin_update"),
    path('admin_movie_form/', views.admin_movie_form, name="admin_movie_form"),
    path('admin_show_form/', views.admin_show_form, name="admin_show_form"),
    path('admin_genre_form/', views.admin_genre_form, name="admin_genre_form"),
    path('admin_artist_form/', views.admin_artist_form, name="admin_artist_form"),
    path('admin_director_form/', views.admin_director_form, name="admin_director_form"),
    path('admin_artist_movie_form/', views.admin_artist_movie_form, name="admin_artist_movie_form"),
    path('admin_artist_show_form/', views.admin_artist_show_form, name="admin_artist_show_form"),
    path('browse_movie_by_genre/', views.browse_by_genre, name="browse_by_genre"),
    path('browse_movie_by_genre/<str:genre>', views.movies_of_genre, name="browse_movie_by_this_genre"),
    path('search_by_year',views.search_by_year, name="search_by_year"),
    path('top_rated_movies', views.top_rated_movies, name = 'top_rated_movies'),
    path('admin_director_movie_form', views.admin_director_movie_form, name="admin_director_movie_form"),
    path('admin_director_show_form', views.admin_director_show_form, name="admin_director_show_form"),
    path('admin_update_artist_death_date_form', views.admin_update_artist_death_date, name="admin_update_artist_death_date_form"),
    path('admin_update_director_death_date_form', views.admin_update_director_death_date, name="admin_update_director_death_date_form"),
    path('admin_update_show_season_form', views.admin_update_show_season, name="admin_update_show_season_form"),
    path('admin_delete_movie', views.admin_delete_movie, name="admin_delete_movie"),
    path('admin_delete_show', views.admin_delete_show, name="admin_delete_show"),
    path('admin_delete_artist', views.admin_delete_artist, name="admin_delete_artist"),
    path('admin_delete_director', views.admin_delete_director, name="admin_delete_director"),
]