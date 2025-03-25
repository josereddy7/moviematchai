# Step 8: create this file and add url next include in the project's urls

from django.urls import path
from .views import MoviesHomeView 
from .views import MoviesDetailView # Step 9
from .views import SearchResultsView # Step 11
from django.views.generic.base import TemplateView # Step 11

urlpatterns = [
    path("movies/", MoviesHomeView.as_view(), name="movies"), 
    path("movies/<pk>", MoviesDetailView.as_view(), name="movie"), # Step 9
    path("search", SearchResultsView.as_view(), name="search"), # Step 11
    path("", TemplateView.as_view(template_name="moviematchapp/home.html"), name="home") # Step 11
]
