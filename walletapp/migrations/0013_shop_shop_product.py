# Generated by Django 5.0.2 on 2024-05-08 13:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0012_remove_detail_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shop_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='walletapp.detail'),
        ),
    ]