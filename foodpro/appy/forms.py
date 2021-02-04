from django import forms
from django.forms import ModelForm

from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'time', 'description', 'image')
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

        def clean_ingredient(self):
            data = self.cleaned_data['ingredient']
            if not data:
                raise forms.ValidationError("You have forgotten about Fred!")
            return data