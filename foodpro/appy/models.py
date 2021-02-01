from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=40, null=True)
    title = models.CharField(max_length=40, null=True)
    style = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='appy/', blank=True, null=True)
    description = models.TextField(blank=False)
    ingredient = models.ManyToManyField(Ingredient,
                                        through='Number',
                                        through_fields=('recipe',
                                                        'ingredient'),
                                        related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    time = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Number(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='numbers')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='numbers')
    amount = models.IntegerField()

    def __str__(self):
        return str(self.amount)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorite_recipes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    def __str__(self):
        return self.recipe.name


class ShopList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shop_list')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shop_list')

    def __str__(self):
        return self.recipe.name
