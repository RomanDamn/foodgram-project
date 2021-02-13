import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import (Favorite, Follow, Number, Recipe, ShopList,
                     Tag, User)
from django.conf import settings


def index(request):
    tag_list = Tag.objects.all()
    tags = request.GET.getlist('tag')
    if tags == []:
        for tag in tag_list:
            tags.append(tag.name)

    recipe_list = Recipe.objects.filter(
        tags__name__in=tags
    ).distinct()

    paginator = Paginator(recipe_list, settings.RECIPES_PER_PAGE)
    in_shop = ShopList.objects.filter(user__username=request.user)
    in_favorite = Favorite.objects.filter(user__username=request.user)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'appy/index.html',
        {'page': page, 'paginator': paginator,
            'in_shop': in_shop, 'in_favorite': in_favorite, 'tag_list': tag_list}
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
    return render(
        request,
        'appy/single_page.html',
        {'recipe': recipe, 'ingredients': ingredients,
            'in_favorite': in_favorite,
        'in_follow': in_follow, 'in_shop': in_shop}
        )


@login_required
def favorites(request):
    tag_list = Tag.objects.all()
    tags = request.GET.getlist('tag')
    if tags == []:
        for tag in tag_list:
            tags.append(tag.name)

    favorite_recipes = Recipe.objects.filter(
        favorites__user=request.user
    ).filter(
        tags__name__in=tags
    ).distinct()
    in_favorite = Favorite.objects.filter(
        user=request.user, recipe=favorite_recipes)
    page_number = request.GET.get('page')
    paginator = Paginator(favorite_recipes, settings.RECIPES_PER_PAGE)
    page = paginator.get_page(page_number)

    return render(
        request,
        'appy/favorite.html', {
            'page': page, 'paginator': paginator,
            'tag_list': tag_list, 'in_favorite': in_favorite
        }
    )


@login_required
def shop_list(request):
    list_shop = Recipe.objects.filter(shop_lists__user=request.user)
    return render(
        request,
        'appy/shop_list.html',
        {'list_shop': list_shop}
    )



@login_required
def get_purchases(request):
    recipes = Recipe.objects.filter(
        shop_lists__user=request.user
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
            name, unit = ingredients[num]
            amount = numbers[num]

            if name in ing:
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
        for tag in tag_list:
            tags.append(tag.name)

    author = get_object_or_404(User, username=username)
    in_follow = Follow.objects.filter(
        user__username=request.user, author__username=username).exists()
    in_favorite = Favorite.objects.filter(user__username=request.user)
    recipes = author.recipes.filter(
        tags__name__in=tags
    ).distinct()
    paginator = Paginator(recipes, settings.RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'appy/author_recipe.html',
        {'author': author, 'page': page,
         'paginator': paginator,
         'tag_list': tag_list, 'in_follow': in_follow, 'in_favorite': in_favorite}
    )



@login_required
def subscriptions_index(request):
    my_following = Follow.objects.filter(user=request.user)
    authors = User.objects.filter(following__in=my_following).order_by('username')
    paginator = Paginator(authors, settings.RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'appy/my_follow.html', {'paginator': paginator,
                                             'page': page})


def about_author(request):
    return render(request, 'about/about_author.html')


def about_tech(request):
    return render(request, 'about/about_tech.html')
