# Generated by Django 5.1 on 2025-03-03 16:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0001_initial'),
        ('products', '0002_productimagemodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlistmodel',
            unique_together={('user', 'product')},
        ),
    ]
