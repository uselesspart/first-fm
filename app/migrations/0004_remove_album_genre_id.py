# Generated by Django 5.0.4 on 2024-04-20 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_album_genre_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='genre_id',
        ),
    ]