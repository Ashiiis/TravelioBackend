# Generated by Django 5.1.1 on 2024-09-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlModels', '0008_alter_citydata_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citydata',
            name='city',
            field=models.CharField(max_length=100),
        ),
    ]