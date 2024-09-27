# Generated by Django 5.1 on 2024-09-16 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('G_rating', models.FloatField()),
                ('reviews', models.IntegerField()),
                ('fee', models.FloatField()),
                ('significance', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=200)),
                ('hotel_price', models.FloatField()),
                ('stars', models.FloatField(blank=True, null=True)),
                ('hotel_rating', models.FloatField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlModels.citydata')),
            ],
        ),
    ]