# myapp/management/commands/import_data.py

import csv
from django.core.management.base import BaseCommand
from Movie.models import TVSeries

class Command(BaseCommand):
    help = 'Imports data from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                TVSeries.objects.create(
                    poster_link=row['Poster_Link'],
                    series_title=row['Series_Title'],
                    released_year=row['Released_Year'],
                    runtime=row['Runtime'],
                    genre=row['Genre'],
                    imdb_rating=row['IMDB_Rating'],
                    overview=row['Overview'],
                    director=row['Director'],
                    star1=row['Star1'],
                    star2=row['Star2'],
                    star3=row['Star3'],
                    star4=row['Star4'],
                    no_of_votes=row['No_of_Votes'],
                    trailer_url=row['trailer_url']

                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
