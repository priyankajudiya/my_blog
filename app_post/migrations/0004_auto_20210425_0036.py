# Generated by Django 3.1.7 on 2021-04-24 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_post', '0003_auto_20210425_0006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_URL',
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='post_images'),
        ),
    ]