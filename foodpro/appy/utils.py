from django.shortcuts import redirect

from .models import Ingredient, Number


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ing_num = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ing_num]
    return ingredients


def save_in_edit_create(request, form):
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        if 'edit' in request.path:
            recipe.numbers.all().delete()
        ingredients = get_ingredients(request)
        for title, numbers in ingredients.items():
            ingredient = Ingredient.objects.get(name=title)
            amount = Number(
                recipe=recipe,
                ingredient=ingredient,
                amount=numbers
            )
            amount.save()

        form.save_m2m()
        return redirect('index')
