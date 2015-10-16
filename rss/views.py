from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import *


def response(data):
    if isinstance(data, list):
        return array_response(data)
    else:
        return single_object_response(data)


def single_object_response(object):
    return JsonResponse(object.__data__())


def array_response(object_array):
    data = list(object.__data__() for object in object_array)
    return JsonResponse(data,
                        safe=False)  # Django serializer won't serialize anything that is not a dict by default


def outlets(request):
    data = get_list_or_404(Outlet.objects.order_by('name'))
    return response(data)


def outlet(request, outlet_id):
    data = get_object_or_404(Outlet, pk=outlet_id)
    return response(data)


def all_authors(request):
    data = get_list_or_404(Author.objects.order_by('name'))
    return response(data)


def authors(request, outlet_id):
    data = get_list_or_404(Author.objects.order_by('name'), outlet_id=outlet_id)
    return response(data)


def author(request, outlet_id, author_id):
    data = get_object_or_404(Author, outlet_id=outlet_id, pk=author_id)
    return response(data)


def all_articles(request):
    data = get_list_or_404(Article.objects.order_by('-pub_date'))
    return response(data)


def articles(request, outlet_id):
    data = get_list_or_404(Article.objects.order_by('-pub_date'), outlet_id=outlet_id)
    return response(data)


def article(request, outlet_id, article_id):
    data = get_object_or_404(Article, id=article_id, outlet_id=outlet_id)
    return response(data)


def tags(request):
    data = get_list_or_404(Tag.objects.order_by('term'))
    return response(data)


def articles_by_tag(request, term):
    data = get_list_or_404(Article.objects.order_by('-pub_date'), tags__term=term)
    return response(data)


def articles_search(request, search):
    search_condition = Q(title__icontains=search) | Q(summary__icontains=search) \
                       | Q(content__icontains=search) | Q(tags__term__icontains=search) \
                       | Q(authors__name__icontains=search)
    data = get_list_or_404(Article.objects.order_by('-pub_date'), search_condition)
    cleaned_data = []
    for article in data:
        if article not in cleaned_data:
            cleaned_data.append(article)
    return response(cleaned_data)