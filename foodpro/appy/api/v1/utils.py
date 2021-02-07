from django.shortcuts import redirect, render

from ...models import Ingredient, Number
from ...utils import get_ingredients


def save_in_edit_create(request, form):
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        if 'edit' in request.path:
            recipe.numbers.all().delete()
            # Без all возникает ошибка
        ingredients = get_ingredients(request)
        for title, numbers in ingredients.items():
            try:
                ingredient = Ingredient.objects.get(name=title)

            except Exception:
                valid = 'Error'
                return render(request, 'form_recipe.html', {'form': form,
                                                            'valid': valid,
                                                            'recipe': recipe
                                                            })
            amount = Number(
                recipe=recipe,
                ingredient=ingredient,
                amount=numbers
            )
            amount.save()

        form.save_m2m()
        return redirect('index')
