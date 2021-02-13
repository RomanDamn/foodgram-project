from django import template
from ..models import Favorite


register = template.Library()


@register.filter(name='is_favorite')
def is_favorite(request, recipe):
    if Favorite.objects.filter(
        user=request.user, recipe=recipe
    ).exists():
        return True

    return False