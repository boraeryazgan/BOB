from django.contrib import admin
from .models import TVSeries, Review, Playlist

# Register your models here.
admin.site.register(TVSeries)
admin.site.register(Review)
admin.site.register(Playlist)