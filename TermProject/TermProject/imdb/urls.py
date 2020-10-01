from django.urls import path

from . import views

app_name = 'imdb'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/', views.movie, name='movie'),
    path('login/', views.login, name="login"),
    path('create_account/', views.create, name="create_account"),
    path('admin_update/', views.admin_update, name="admin_update"),
    path('admin_movie_form/', views.admin_movie_form, name="admin_movie_form"),
    path('admin_show_form/', views.admin_show_form, name="admin_show_form"),
    path('admin_genre_form/', views.admin_genre_form, name="admin_genre_form"),
    path('admin_artist_form/', views.admin_artist_form, name="admin_artist_form"),
    path('admin_director_form/', views.admin_director_form, name="admin_director_form"),
]


