# Generated by Django 5.1.1 on 2024-09-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlModels', '0004_citydata_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citydata',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
