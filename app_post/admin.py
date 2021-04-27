from django.contrib import admin
from app_post import models
# Register your models here.

@admin.register(models.Post)
class PostAdminModel(admin.ModelAdmin):
    list_display = ['author','title', 'slug','img_URL']


@admin.register(models.Comment)
class CommentAdminModel(admin.ModelAdmin):
    list_display = ['name','email','comment','post']