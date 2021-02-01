from django import forms
from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tags', "time", "description", "image",)
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
