# Generated by Django 5.1 on 2025-03-10 18:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_commentmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='rating',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating'),
        ),
    ]
