# Generated by Django 5.0.4 on 2024-05-01 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_groupappointment_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='training_plan',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='user',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]