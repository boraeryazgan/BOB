# Generated by Django 5.0.2 on 2024-03-08 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TVSeries",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("poster_link", models.CharField(max_length=255)),
                ("series_title", models.CharField(max_length=255)),
                ("released_year", models.CharField(max_length=4)),
                ("runtime", models.CharField(max_length=10)),
                ("genre", models.CharField(max_length=255)),
                ("imdb_rating", models.FloatField()),
                ("overview", models.TextField()),
                ("director", models.CharField(max_length=255)),
                ("star1", models.CharField(max_length=255)),
                ("star2", models.CharField(max_length=255)),
                ("star3", models.CharField(max_length=255)),
                ("star4", models.CharField(max_length=255)),
                ("no_of_votes", models.IntegerField()),
                ("trailer_url", models.URLField(default="", null=True)),
            ],
        ),
    ]
