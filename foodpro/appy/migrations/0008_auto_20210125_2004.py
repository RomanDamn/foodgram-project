# Generated by Django 2.2 on 2021-01-25 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appy', '0007_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(related_name='recipes', through='appy.Number', to='appy.Ingredient'),
        ),
    ]
