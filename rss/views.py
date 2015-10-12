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