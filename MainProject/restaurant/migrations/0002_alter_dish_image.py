# Generated by Django 5.1.3 on 2024-11-30 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, default='\\product_images\\download_1.jpg', null=True, upload_to='product_images/'),
        ),
    ]
