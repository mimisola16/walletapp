# Generated by Django 3.2.3 on 2024-05-31 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('walletapp', '0007_auto_20240601_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=11, max_length=300),
            preserve_default=False,
        ),
    ]