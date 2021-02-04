from django.urls import path

from . import views as view
from .api.v1 import views

urlpatterns = [
    path(
        'change-favorites/<int:recipe_id>/',
        views.change_favorites,
        name='change_favorites'
    ),
    path(
        'subscriptions-button/<int:author_id>/',
        views.subscriptions_button,
        name='subscriptions_button'
    ),
    path('purchases/<int:recipe_id>/',
         views.purchases, name='purchases'),
    path('get-purchases/', view.get_purchases, name='get_purchases')
]

urlpatterns += [
    path('', view.index, name='index'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('subscriptions/', view.subscriptions_index, name='subscriptions'),
    path('favorites/', view.favorites, name='favorites'),
    path('shop-list/', views.shop_list, name='shop_list'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('about-author/', view.about_author, name='about_author'),
    path('about-tech/', view.about_tech, name='tech'),
    path('<str:username>/', view.author_recipes, name='author_recipes'),
    path('<str:username>/<int:id>/', view.recipe_view, name='recipe_view'),
    path('<str:username>/<int:id>/edit/',
         views.edit_recipe, name='edit_recipe'),
    path('<str:username>/<int:id>/delete/',
         views.delete_recipe, name='delete_recipe'),
]
