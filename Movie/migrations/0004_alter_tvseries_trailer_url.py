# Generated by Django 5.0.2 on 2024-03-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Movie", "0003_alter_tvseries_trailer_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tvseries",
            name="trailer_url",
            field=models.CharField(default="", max_length=255, null=True),
        ),
    ]