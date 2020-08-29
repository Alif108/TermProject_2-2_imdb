from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "imdb/index.html")

def movie(request):
    return render(request, "imdb/movies.html")

def login(request):
    return render(request, "imdb/login.html")

def create(request):
    return render(request, "imdb/create_account.html")