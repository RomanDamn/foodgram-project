from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Favorite, Ingredient, Recipe

User = get_user_model()


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "recipe_favorites")
    search_fields = ("author",)
    list_filter = ("author", "name", "tags", 'ingredient')

    def recipe_favorites(self, obj):
        result = Favorite.objects.filter(recipe=obj).count()
        return result


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", 'unit')
    list_filter = ("name",)


class MyUserAdmin(UserAdmin):
    list_filter = ('email', 'first_name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
