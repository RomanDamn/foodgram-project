import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.views.decorators.http import require_http_methods

from ...forms import RecipeForm
from ...models import Favorite, Recipe, ShopList, Number, Ingredient, Follow, User
from ...utils import get_ingredients
from ...views import shop_list


@login_required
@require_http_methods(['POST', 'DELETE'])
def change_favorites(request, recipe_id):
    status = True
    if request.method == 'POST':
        id = json.loads(request.body).get('id')
        recipe = get_object_or_404(
            Recipe, pk=id
        )
        obj, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )

        if not created:
            status = False
            return JsonResponse({'success': status})

        return JsonResponse({'success': status})

    else:
        recipe = get_object_or_404(
            Recipe, pk=recipe_id
        )

        removed = Favorite.objects.filter(
            recipe=recipe, user=request.user
        ).delete()


        if removed:
            return JsonResponse({'success': status})
        status = False
        return JsonResponse({'success': status})


@login_required
@require_http_methods(['POST', 'DELETE', 'GET'])
def purchases(request, recipe_id):
    status = True
    if request.method == "POST":
        id = json.loads(request.body).get('id')
        recipe = get_object_or_404(
            Recipe, pk=id
        )

        obj, created = ShopList.objects.get_or_create(
            user=request.user, recipe=recipe
        )

        if not created:
            status = False
            return JsonResponse({'success': status})

        return JsonResponse({'success': status})

    elif request.method in ['GET', 'DELETE']:
        ShopList.objects.filter(
            user=request.user, recipe=recipe_id
        ).delete()
        if request.method == 'GET':
            return redirect(shop_list)



@login_required
def create_recipe(request):
    if request.method == 'POST':
        ing = [v for k, v in request.POST.items() if k.startswith('nameIngredient_')]
        form = RecipeForm(request.POST, files=request.FILES or None)
        if len(ing) == 0:
            valid = 'error'
            return render(request, 'form_recipe.html', {'form': form,
                                                       'valid': valid})
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

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
        valid = 'error'
        return render(request, 'form_recipe.html', {'form': form,
                                                   'valid': valid})
    form = RecipeForm(request.POST, files=request.FILES or None)
    return render(request, 'form_recipe.html', {'form': form})


'''
 мне показалось что при объединении вюшек edit_recipe и create_recipe 
 и двух шаблонов ухудшается читабельность кода и появляется много условий в шаблонах.
 Может в конкретном случае и не обязательно объединять эти две вьюшки и 2 шаблона?
'''


@login_required
def edit_recipe(request, username, id):
    recipe = get_object_or_404(Recipe, author__username=username, id=id)
    if request.method == 'POST':
        form = RecipeForm(request.POST,
                          files=request.FILES or None, instance=recipe)
        if form.is_valid():
            this_recipe = form.save(commit=False)
            this_recipe.author = request.user
            this_recipe.save()
            this_recipe.numbers.all().delete()
            ingredients = get_ingredients(request)

            for title, numbers in ingredients.items():
                ingredient = Ingredient.objects.get(name=title)
                amount = Number(
                    recipe=this_recipe,
                    ingredient=ingredient,
                    amount=numbers
                )
                amount.save()

            form.save_m2m()
            return redirect('index')
        valid = 'error'
        return render(request, 'form_change_recipe.html', {'form': form,
                                                         'recipe': recipe,
                                                         'valid': valid})
    form = RecipeForm(request.POST,
                      files=request.FILES or None,
                      instance=recipe)
    return render(request, 'form_change_recipe.html',
                  {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, username, id):
    recipe = get_object_or_404(Recipe, pk=id, author__username=username)
    recipe.delete()
    return redirect("index")


@login_required
@require_http_methods(["POST", "DELETE"])
def subscriptions_button(request, author_id):
    status = True
    if request.method == "POST" and author_id != request.user.id:
        id = json.loads(request.body).get('id')
        author = get_object_or_404(
            User, pk=id
        )

        obj, created = Follow.objects.get_or_create(
            user=request.user, author=author
        )

        if not created:
            status = False
            return JsonResponse({'success': status})

        return JsonResponse({'success': status})


    else:
        author = get_object_or_404(User, id=author_id)

        removed = Follow.objects.filter(
            user=request.user, author=author
        ).delete()

        if removed:
            return JsonResponse({'success': status})
        status = False
        return JsonResponse({'success': status})


def ingredients(request):
    text = request.GET.get('query')
    ingredients_list = Ingredient.objects.filter(name__istartswith=text)
    listy = []

    for ingredient in ingredients_list:
        dicty = {}
        dicty['title'] = ingredient.name
        dicty['dimension'] = ingredient.unit
        listy.append(dicty)
    return JsonResponse(listy, safe=False)
