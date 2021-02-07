import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.views.decorators.http import require_http_methods

from ...forms import RecipeForm
from ...models import (Favorite, Recipe, ShopList,
                       Ingredient, Follow, User)
from .utils import save_in_edit_create
from ...views import shop_list


@login_required
@require_http_methods(['POST', 'DELETE'])
def change_favorites(request, recipe_id):
    status = False
    recipe = get_object_or_404(
        Recipe, pk=recipe_id)
    if request.method == 'POST':
        obj, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )

        if created:
            status = True
        return JsonResponse({'success': status})

    removed = Favorite.objects.filter(
        recipe=recipe, user=request.user
    ).delete()

    if removed:
        status = True
    return JsonResponse({'success': status})


@login_required
@require_http_methods(['POST', 'DELETE', 'GET'])
def purchases(request, recipe_id):
    status = False
    if request.method == "POST":
        id = json.loads(request.body).get('id')
        recipe = get_object_or_404(
            Recipe, pk=id
        )

        obj, created = ShopList.objects.get_or_create(
            user=request.user, recipe=recipe
        )

        if created:
            status = True
        return JsonResponse({'success': status})

    removed = ShopList.objects.filter(
        user=request.user, recipe=recipe_id
    ).delete()

    if request.method == 'GET':
        return redirect(shop_list)

    if removed:
        status = True
    return JsonResponse({'success': status})


def server_error(request):
    return HttpResponse("500 error", status_code=404)


@login_required
def edit_recipe(request, username, id):
    recipe = get_object_or_404(Recipe, author__username=username, id=id)
    if request.method == 'POST':
        form = RecipeForm(request.POST,
                          files=request.FILES or None, instance=recipe)
        if form.is_valid():
            return save_in_edit_create(request, form)
        valid = 'error'
        return render(request, 'appy/form_recipe.html', {'form': form,
                                                    'valid': valid,
                                                    'recipe': recipe
                                                    })

    form = RecipeForm(request.POST,
                      files=request.FILES or None,
                      instance=recipe)
    return render(request, 'appy/form_recipe.html',
                  {'form': form, 'recipe': recipe})


@login_required
def create_recipe(request):
    if request.method == 'POST':
        ing = [ing for key,
               ing in request.POST.items()
               if key.startswith('nameIngredient_')]

        form = RecipeForm(request.POST, files=request.FILES or None)
        if len(ing) == 0:
            valid = 'error'
            return render(request, 'appy/form_recipe.html', {'form': form,
                                                        'valid': valid,
                                                        })
        if form.is_valid():
            return save_in_edit_create(request, form)
        valid = 'error'
        return render(request, 'appy/form_recipe.html', {'form': form,
                                                    'valid': valid,
                                                    })

    form = RecipeForm(request.POST, files=request.FILES or None)
    return render(request, 'appy/form_recipe.html', {'form': form})


@login_required
def delete_recipe(request, username, id):
    recipe = get_object_or_404(Recipe, pk=id, author__username=username)
    recipe.delete()
    return redirect("appy/index")


@login_required
@require_http_methods(["POST", "DELETE"])
def subscriptions_button(request, author_id):
    status = False
    author = get_object_or_404(
        User, pk=author_id)
    if request.method == "POST" and author_id != request.user.id:

        obj, created = Follow.objects.get_or_create(
            user=request.user, author=author
        )

        if created:
            status = True
        return JsonResponse({'success': status})

    removed = Follow.objects.filter(
        user=request.user, author=author
    ).delete()

    if removed:
        status = True
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
