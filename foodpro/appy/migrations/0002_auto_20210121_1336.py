# Generated by Django 2.2 on 2021-01-21 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(related_name='ing', through='appy.Number', to='appy.Ingredient'),
        ),
    ]
