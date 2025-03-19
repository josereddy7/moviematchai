from django.shortcuts import render

# Create your views here.

# Step 7: Create the view for displaying movies then create the templates folder and add the home template:
# Step 9: create detail view, template and url
# Step 10: add get similar movies to Movie model and call it in get_contex_data then add it to the template and iterate over and display similar movies
# Step 11: add home url with a template that renders a search form; then add a search view for movies based on atlas search. First create a form for search, then create a template and add it to it then the view
from django.views.generic import ListView
from django.views.generic.detail import DetailView # Step 9

from .models import Movie



class MoviesHomeView(ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 4

# Step 9 
class MoviesDetailView(DetailView):
    model = Movie  
    context_object_name = 'movie'  
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        print("Getting similar movies")
        context["movies"]= self.get_object().get_similar_movies() 
        return context
    
# Step 11
class SearchResultsView2(ListView):
    template_name = 'moviematchapp/search_results.html'
    context_object_name = 'movies'
    model = Movie

    def get_queryset(self):
        query = self.request.GET.get('q') or ''
        title = self.request.GET.get('title') or ''
        actor = self.request.GET.get('actor') or ''
        genre = self.request.GET.get('genre') or ''
        print('query : ' + query +  ' ' + title + ' ' + actor + ' ' + genre)
        if query:
            pipeline = [
                {
                    "$search": {
                        "index": "fullplot_index",
                        "compound": {
                            "should": [
                                { "text": { "query": title, "path": "title", "score": { "boost": { "value": 3 } } } },
                                { "text": { "query": actor, "path": "cast", "score": { "boost": { "value": 2 } } } },
                                { "text": { "query": genre, "path": "genres", "score": { "boost": { "value": 1.5 } } } },
                                { "text": { "query": query, "path": "fullplot" } }
                            ],
                            "minimumShouldMatch": 1
                        }
                    }
                },
                { "$limit": 20 },
                { 
                    "$project": {
                        "_id": 1,
                        "title": 1,
                        "poster":1,
                        }
                 },
            ]
            object_list = Movie.objects.raw_aggregate(pipeline)
            print(object_list)
        else:
            object_list = self.model.objects.none()
        return object_list
    


class SearchResultsView(ListView):
    template_name = 'moviematchapp/search_results.html'
    context_object_name = 'movies'
    model = Movie

    def get_queryset(self):
        query = self.request.GET.get('q') or ''
        title = self.request.GET.get('title') or ''
        actor = self.request.GET.get('actor') or ''
        genre = self.request.GET.get('genre') or ''
        
        print(f'Query: {query}, Title: {title}, Actor: {actor}, Genre: {genre}')
        
        if query or title or actor or genre:
            pipeline = [
                {
                    "$search": {
                        "index": "fullplot_index",
                        "compound": {
                            "should": [
                                { 
                                    "text": { 
                                        "query": title, 
                                        "path": "title", 
                                        "score": { "boost": { "value": 5 } } 
                                    } 
                                } if title else None,
                                { 
                                    "text": { 
                                        "query": actor, 
                                        "path": "cast", 
                                        "score": { "boost": { "value": 3 } } 
                                    } 
                                } if actor else None,
                                { 
                                    "text": { 
                                        "query": genre, 
                                        "path": "genres", 
                                        "score": { "boost": { "value": 2 } } 
                                    } 
                                } if genre else None,
                                { 
                                    "text": { 
                                        "query": query, 
                                        "path": ["fullplot", "title"],  # Search multiple fields
                                        "fuzzy": { "maxEdits": 1 },  # Allow minor typos
                                        "score": { "boost": { "value": 1 } }
                                    } 
                                } if query else None
                            ],
                            "minimumShouldMatch": 1
                        }
                    }
                },
                { "$limit": 20 },
                { 
                    "$project": {
                        "_id": 1,
                        "title": 1,
                        "poster": 1,
                        "score": { "$meta": "searchScore" }  # Include search score for ranking
                    }
                },
                { "$sort": { "score": -1 } }  # Sort results by relevance
            ]

            # Remove None values from pipeline (if title, actor, or genre are empty)
            pipeline[0]["$search"]["compound"]["should"] = [
                condition for condition in pipeline[0]["$search"]["compound"]["should"] if condition
            ]

            # Ensure the pipeline still works if everything was removed
            if not pipeline[0]["$search"]["compound"]["should"]:
                return self.model.objects.none()
            
            # Use Django MongoDB Model execute aggregation
            try:
                object_list = list(Movie.objects.raw_aggregate(pipeline))  
            except AttributeError:
                object_list = []  
            
            print(object_list)

        else:
            object_list = self.model.objects.none()
        
        return object_list  # Returning processed queryset or empty queryset
