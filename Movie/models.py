from django.db import models
class TVSeries(models.Model):
    poster_link = models.CharField(max_length=255)
    series_title = models.CharField(max_length=255)
    released_year = models.CharField(max_length=4)
    runtime = models.CharField(max_length=10)
    genre = models.CharField(max_length=255)
    imdb_rating = models.FloatField()
    overview = models.TextField()
    director = models.CharField(max_length=255)
    star1 = models.CharField(max_length=255)
    star2 = models.CharField(max_length=255)
    star3 = models.CharField(max_length=255)
    star4 = models.CharField(max_length=255)
    no_of_votes = models.IntegerField()
    trailer_url = models.CharField(null=True,default="",max_length=255)


    def __str__(self):
        return self.series_title