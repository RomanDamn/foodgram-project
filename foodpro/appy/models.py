from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента',
                            max_length=50)
    unit = models.CharField('Единица измерения',
                            max_length=50)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.SlugField('Слаг',
                            max_length=40, unique=True)
    title = models.CharField('Название тэга на русском',
                             max_length=40, null=True)
    style = models.CharField('Стиль',
                             max_length=50, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='author')
    name = models.CharField('Название рецепта', max_length=40)
    image = models.ImageField(upload_to='appy/',
                              blank=True, null=True,
                              verbose_name='Изображение')
    description = models.TextField('Описание', blank=False)
    ingredient = models.ManyToManyField(Ingredient,
                                        through='Number',
                                        through_fields=('recipe',
                                                        'ingredient'),
                                        related_name='recipes',
                                        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Тэги')
    time = models.PositiveIntegerField('Время приготовления',
                                       validators=[MinValueValidator(1), ])
    pub_date = models.DateTimeField('Время публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Number(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='numbers',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='numbers',
                                   verbose_name='Ингредиент')
    amount = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'Количество'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return str(self.amount)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower", verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following", verbose_name='Автор'
    )

    class Meta:
        unique_together = ['user', 'author']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='user_author'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='forbidden_fol_yourself'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name='Пользователь'
    )

    class Meta:
        unique_together = ['recipe', 'user']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return self.recipe.name


class ShopList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shop_lists',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shop_lists',
                               verbose_name='Рецепт')

    class Meta:
        unique_together = ['user', 'recipe']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return self.recipe.name
