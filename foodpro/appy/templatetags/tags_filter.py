from django import template

register = template.Library()


@register.filter()
def get_tag_url(request, tag):
    new_request = request.GET.copy()
    if tag.name in request.GET.getlist('tag'):
        tags = new_request.getlist('tag')
        tags.remove(tag.name)
        new_request.setlist('tag', tags)
    else:
        new_request.appendlist('tag', tag.name)

    return new_request.urlencode()
