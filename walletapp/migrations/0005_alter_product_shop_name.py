# Generated by Django 3.2.3 on 2024-05-31 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0004_remove_shop_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shop_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='walletapp.shop', verbose_name='Shop Name'),
        ),
    ]
