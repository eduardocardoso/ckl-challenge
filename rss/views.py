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


def authors(request, outlet_id):
    data = get_list_or_404(Author.objects.order_by('name'), outlet_id=outlet_id)
    return response(data)


def author(request, outlet_id, author_id):
    data = get_object_or_404(Author, outlet_id=outlet_id, pk=author_id)
    return response(data)


def articles(request, outlet_id):
    data = get_list_or_404(Article.objects.order_by('-pub_date'), outlet_id=outlet_id)
    return response(data)

def article(request, outlet_id, article_id):
    data = get_object_or_404(Article, id=article_id, outlet_id=outlet_id)
    return response(data)