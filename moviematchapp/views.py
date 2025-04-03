from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView
from django.views.generic.detail import DetailView # Step 9

from .models import Movie



class MoviesHomeView(ListView):
    model = Movie
    context_object_name = 'movies'
    paginate_by = 4


class MoviesDetailView(DetailView):
    model = Movie  
    context_object_name = 'movie'  
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        print("Getting similar movies")
        context["movies"]= self.get_object().get_similar_movies() 
        return context
    
    
class SearchResultsView(ListView):
    template_name = 'moviematchapp/search_results.html'
    context_object_name = 'movies'
    model = Movie

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        title = self.request.GET.get('title', '').strip()
        actor = self.request.GET.get('actor', '').strip()
        
        print(f'Query: {query}, Title: {title}, Actor: {actor}')
        
        # If no search parameters are provided, return empty queryset
        if not any([query, title, actor]):
            return self.model.objects.none()
        
        # Construct pipeline with search conditions
        pipeline = [
            {
                "$search": {
                    "index": "default",
                    "compound": {
                        "should": []
                    }
                }
            },
            {"$limit": 20},
            { 
                "$project": {
                    "_id": 1
                }
            },
            {"$sort": {"score": -1}}
        ]
        
        # Dynamically add search conditions
        search_conditions = []
        if title and len(title) > 0:
            search_conditions.append({ 
                "phrase": { 
                    "query": title, 
                    "path": "title", 
                    "score": {"boost": {"value": 3}} 
                } 
            })
        
        if actor and len(actor) > 0:
            search_conditions.append({ 
                "phrase": { 
                    "query": actor, 
                    "path": "cast", 
                    "score": {"boost": {"value": 1}} 
                } 
            })

        if query and len(query) > 0:
            search_conditions.append({ 
                "text": { 
                    "query": query, 
                    "path": ["fullplot"],
                    "fuzzy": {"maxEdits": 1},
                    "score": {"boost": {"value": 4}}
                } 
            })
        
        # Only add conditions if they exist
        if search_conditions:
            pipeline[0]["$search"]["compound"]["should"] = search_conditions
        else:
            return self.model.objects.none()
        
        # Execute aggregation
        try:
            object_list = list(Movie.objects.raw_aggregate(pipeline))
            print("Search Results:", object_list)
            return object_list
        except Exception as e:
            print(f"Search Error: {e}")
            return self.model.objects.none()