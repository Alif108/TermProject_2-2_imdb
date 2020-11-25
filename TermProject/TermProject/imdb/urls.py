from django.urls import path

from . import views

app_name = 'imdb'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<str:movie>', views.movie, name='movie'),
    path('artist/<str:actor>', views.artist, name='artist'),
    path('artist/<str:director>', views.artist, name='director'),
    path('login/', views.login, name="login"),
    path('create_account/', views.create, name="create_account"),
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
    path('admin_director_movie_form', views.admin_director_movie_form, name="admin_director_movie_form"),
    path('admin_director_show_form', views.admin_director_show_form, name="admin_director_show_form"),

]