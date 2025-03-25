from django.db import models
from django_mongodb_backend.fields import ArrayField
from django_mongodb_backend.managers import MongoManager # Step 10


    


class Movie(models.Model):
    title = models.CharField(max_length=200)
    plot = models.TextField(blank=True)
    fullplot = models.TextField(blank=True)
    plot_embedding = ArrayField(models.FloatField())
    poster =  models.URLField()
    runtime = models.IntegerField(default=0)
    released = models.DateTimeField("release date", null=True, blank=True)
    cast = ArrayField(models.CharField(max_length=200))
    genres = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    objects = MongoManager() # Step 10 Custom manager for MongoDB support


    # step 10
    def get_similar_movies(self):
        """Finds the most similar movies using vector search on plot embeddings."""

        if not self.plot_embedding:
            return []  # Return empty list if there's no embedding to prevent query errors

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "plot_embedding",
                    "queryVector": self.plot_embedding,
                    "numCandidates": 100, 
                    "limit": 5  # Return top 5 most similar movies
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "poster": 1,
                    "score": { "$meta": "vectorSearchScore" }  # Include similarity score
                }
            },
            { "$sort": { "score": -1 } }  # Sort results by similarity score
        ]

        try:
            return list(Movie.objects.raw_aggregate(pipeline))  # Ensure results are returned as a list
        except:
            return []  


    class Meta:
        db_table = "embedded_movies"
        managed = False

    def __str__(self):
        return self.title
