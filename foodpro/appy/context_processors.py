from .models import ShopList


def shop_list_count(request):
    if request.user.is_authenticated:
        list_count = ShopList.objects.filter(
            user=request.user
        ).count()
    else:
        list_count = None

    return {'list_count': list_count}
