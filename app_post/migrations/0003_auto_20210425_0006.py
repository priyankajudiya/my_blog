# Generated by Django 3.1.7 on 2021-04-24 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_post', '0002_post_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images'),
        ),
    ]