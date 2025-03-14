# Generated by Django 5.1 on 2025-03-09 12:21

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_addressmodel'),
        ('e_commerce', '0004_alter_cartmodel_unique_together'),
        ('products', '0003_commentmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('shipping_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='account.addressmodel', verbose_name='shipping_address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='cost')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('payment_received', 'Payment Received'), ('processing', 'Processing'), ('packaged', 'Packaged'), ('shipped', 'Shipped'), ('out_for_delivery', 'Out for Delivery'), ('in_the_local_delivery_center', 'In the Local Delivery Center'), ('given_to_courier', 'Given to Courier'), ('delivered', 'Delivered')], default='pending', verbose_name='status')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='details', to='products.productmodel', verbose_name='product')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='e_commerce.ordermodel', verbose_name='order')),
            ],
            options={
                'verbose_name': 'Order_detail',
                'verbose_name_plural': 'Order details',
                'db_table': 'order_detail',
            },
        ),
    ]
