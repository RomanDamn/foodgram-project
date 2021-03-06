# Generated by Django 2.2 on 2021-02-07 15:01

import django.core.validators
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('appy', '0021_auto_20210205_2234'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique follows',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='user_author'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='forbidden_fol_yourself'),
        ),
    ]
