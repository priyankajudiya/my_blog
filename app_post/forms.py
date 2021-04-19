from django import forms
from django.db.models import fields
from django.forms import ModelForm
from app_user import models


class commentForm(ModelForm):
    class Meta():
        model = models.Comment
        fields = 'name', 'email', 'comment'
