# Generated by Django 5.1 on 2025-02-22 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storemodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='storemodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='modified_at'),
        ),
    ]
