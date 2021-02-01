import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import RecipeForm
from .models import (Favorite, Follow, Ingredient, Number, Recipe, ShopList,
                     Tag, User)
from .utils import get_ingredients


def index(request):
    tag_list = Tag.objects.all()
    tags = request.GET.getlist('tag')
    if tags == []:
        tags = ['breakfast', 'lunch', 'dinner', 'cocktail']
    recipe_list = Recipe.objects.filter(
        tags__name__in=tags
    ).distinct()

    paginator = Paginator(recipe_list, 6)
    in_shop = ShopList.objects.filter(user__username=request.user)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        return render(
            request,
            'indexAuth.html',
            {'page': page, 'paginator': paginator,
             'in_shop': in_shop, 'tag_list': tag_list}
        )
    return render(
        request,
        'indexNotAuth.html',
        {'page': page, 'paginator': paginator}
    )


def recipe_view(request, username, id):
    recipe = get_object_or_404(Recipe, id=id, author__username=username)
    in_favorite = Favorite.objects.filter(
        user__username=request.user, recipe=recipe).exists()
    in_follow = Follow.objects.filter(
        user__username=request.user, author__username=username).exists()
    in_shop = ShopList.objects.filter(user__username=request.user,
                                      recipe__name=recipe).exists()
    ingredients = Number.objects.filter(recipe=recipe)
    if request.user.is_authenticated:
        return render(
            request,
            'singlePage.html',
            {'recipe': recipe, 'ingredients': ingredients,
             'in_favorite': in_favorite,
            'in_follow': in_follow, 'in_shop': in_shop}
        )
    return render(
        request,
        'singlePageNotAuth.html',
        {'recipe': recipe, 'ingredients': ingredients}
    )


@login_required
def favorites(request):
    tag_list = Tag.objects.all()
    tags = request.GET.getlist('tag')
    if tags == []:
        tags = ['breakfast', 'lunch', 'dinner', 'cocktail']

    favorite_recipes = Recipe.objects.filter(
        favorite_recipes__user=request.user
    ).filter(
        tags__name__in=tags
    ).distinct()
    in_favorite = Favorite.objects.filter(
        user=request.user, recipe=favorite_recipes)
    page_number = request.GET.get('page')
    paginator = Paginator(favorite_recipes, 6)
    page = paginator.get_page(page_number)

    return render(
        request,
        'favorite.html', {
            'page': page, 'paginator': paginator,
            'tag_list': tag_list, 'in_favorite': in_favorite
        }
    )


@login_required
@require_http_methods(["POST", "DELETE"])
def change_favorites(request, recipe_id):
    if request.method == "POST":
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(
            Recipe, pk=recipe_id
        )
        obj, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )

        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})

    elif request.method == "DELETE":
        recipe = get_object_or_404(
            Recipe, pk=recipe_id
        )

        removed = Favorite.objects.filter(
            recipe=recipe, user=request.user
        ).delete()

        if removed:
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


def shop_list(request):
    list_shop = Recipe.objects.filter(shop_list__user=request.user)
    return render(
        request,
        'shopList.html',
        {'list_shop': list_shop}
    )


@login_required
def purchases(request, recipe_id):
    if request.method == "POST":
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(
            Recipe, pk=recipe_id
        )

        obj, created = ShopList.objects.get_or_create(
            user=request.user, recipe=recipe
        )

        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})

    elif request.method in ["DELETE", "GET"]:

        removed = ShopList.objects.filter(
            user=request.user, recipe=recipe_id
        ).delete()

        if request.method == 'GET':
            return redirect(shop_list)

        if removed:
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


@login_required
def get_purchases(request):
    recipes = Recipe.objects.filter(
        shop_list__user=request.user
    )

    ing: dict = {}

    for recipe in recipes:
        ingredients = recipe.ingredient.values_list(
            'name', 'unit'
        )
        numbers = recipe.numbers.values_list(
            'amount', flat=True
        )

        for num in range(len(ingredients)):
            name = ingredients[num][0]
            unit = ingredients[num][1]
            amount = numbers[num]

            if name in ing.keys():
                ing[name] = [ing[name][0] + amount, unit]
            else:
                ing[name] = [amount, unit]

    response = HttpResponse(content_type='txt/csv')
    response['Content-Disposition'] = 'attachment; filename="shop_list.txt"'
    writer = csv.writer(response)

    for key, value in ing.items():
        writer.writerow([f'{key} ({value[1]}) - {value[0]}'])
    return response


def author_recipes(request, username):
    tag_list = Tag.objects.all()
    tags = request.GET.getlist('tag')
    if tags == []:
        tags = ['breakfast', 'lunch', 'dinner', 'cocktail']

    author = get_object_or_404(User, username=username)
    in_follow = Follow.objects.filter(
        user__username=request.user, author__username=username).exists()
    recipes = author.recipes.filter(
        tags__name__in=tags
    ).distinct()
    paginator = Paginator(recipes, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'authorRecipe.html',
        {'recipes': recipes, 'page': page,
         'paginator': paginator, 'author': author,
         'tag_list': tag_list, 'in_follow': in_follow}
    )


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, files=request.FILES or None)
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
        return render(request, 'formRecipe.html', {'form': form,
                                                   'valid': valid})
    form = RecipeForm(request.POST, files=request.FILES or None)
    return render(request, 'formRecipe.html', {'form': form})


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
        return render(request, 'formChangeRecipe.html', {'form': form,
                                                         'recipe': recipe,
                                                         'valid': valid})
    form = RecipeForm(request.POST,
                      files=request.FILES or None,
                      instance=recipe)
    return render(request, 'formChangeRecipe.html',
                  {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, username, id):
    recipe = get_object_or_404(Recipe, pk=id)
    recipe.delete()
    return redirect("index")

@login_required
def subscriptions_index(request):
    my_following = Follow.objects.filter(user=request.user).all()
    authors = User.objects.filter(following__in=my_following).order_by('username')
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {'paginator': paginator,
                                             'page': page})


@login_required
@require_http_methods(["POST", "DELETE"])
def subscriptions_button(request, author_id):
    if request.method == "POST":
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(
            User, pk=author_id
        )

        obj, created = Follow.objects.get_or_create(
            user=request.user, author=author
        )

        if not created:
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})


    elif request.method == "DELETE":
        author = get_object_or_404(User, id=author_id)

        removed = Follow.objects.filter(
            user=request.user, author=author
        ).delete()

        if removed:
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


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
