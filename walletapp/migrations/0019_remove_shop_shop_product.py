# Generated by Django 5.0.2 on 2024-05-08 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0018_detail_created_at_detail_uploaded_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='shop_product',
        ),
    ]
