# Generated by Django 3.1.7 on 2021-04-24 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0005_remove_post_cropping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
