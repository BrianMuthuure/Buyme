# Generated by Django 4.2.1 on 2023-05-28 12:20

import apps.products.common
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=apps.products.common.user_directory_path, verbose_name='Image'),
        ),
    ]
