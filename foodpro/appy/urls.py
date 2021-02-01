from django.urls import path

from . import views

urlpatterns = [
    path(
        "change_favorites/<int:recipe_id>",
        views.change_favorites,
        name="change_favorites"
    ),
    path(
        "subscriptions_button/<int:author_id>",
        views.subscriptions_button,
        name="subscriptions_button"
    ),
    path("purchases/<int:recipe_id>",
         views.purchases, name="purchases"),
    path("get_purchases", views.get_purchases, name="get_purchases")
]

urlpatterns += [
    path('', views.index, name='index'),
    path("ingredients", views.ingredients, name="ingredients"),
    path('subscriptions/', views.subscriptions_index, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('shop-list/', views.shop_list, name='shop_list'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('<str:username>/', views.author_recipes, name='author_recipes'),
    path('<str:username>/<int:id>/', views.recipe_view, name='recipe_view'),
    path('<str:username>/<int:id>/edit',
         views.edit_recipe, name='edit_recipe'),
    path('<str:username>/<int:id>/delete',
         views.delete_recipe, name='delete_recipe'),
]
