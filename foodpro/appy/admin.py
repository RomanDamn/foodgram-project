from django.contrib import admin
from .models import Favorite, Ingredient, Recipe, Number


class IngredientInline(admin.TabularInline):
    model = Number
    min_num = 1
    extra = 0
    verbose_name = 'ингредиент'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'recipe_favorites')
    search_fields = ('author',)
    list_filter = ('author', 'name', 'tags', 'ingredient')

    inlines = [
        IngredientInline,
    ]

    def recipe_favorites(self, obj):
        result = Favorite.objects.filter(recipe=obj).count()
        return result

    recipe_favorites.short_description = 'Favorites'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
