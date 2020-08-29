from django.urls import path

from . import views

app_name = 'imdb'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/', views.movie, name='movie'),
    path('login/', views.login, name="login"),
    path('create_account/', views.create, name="create_account"),
]


