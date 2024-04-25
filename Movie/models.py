from django.db import models
from django.contrib.auth.models import User

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

class Review(models.Model):
    user = models.ForeignKey(User,models.CASCADE)
    tv_serie = models.ForeignKey(TVSeries,models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - Comment by {self.user.username} at {self.tv_serie.series_title}"

class Playlist(models.Model):
    title = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(TVSeries)
    is_like_playlist = models.BooleanField()

    def __str__(self):
        return self.title