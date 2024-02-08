# Generated by Django 5.0.2 on 2024-02-08 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0011_remove_travel_destination_destination_travel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='travel',
        ),
        migrations.AddField(
            model_name='travel',
            name='destination',
            field=models.ManyToManyField(to='travel_app.destination'),
        ),
    ]
