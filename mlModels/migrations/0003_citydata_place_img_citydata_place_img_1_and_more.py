# Generated by Django 5.1 on 2024-09-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlModels', '0002_alter_citydata_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='citydata',
            name='place_img',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='citydata',
            name='place_img_1',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='citydata',
            name='place_img_2',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='citydata',
            name='place_img_3',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='citydata',
            name='place_img_4',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
