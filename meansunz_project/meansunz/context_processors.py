# main/context_processors.py
from django.conf import settings

from meansunz.models import Category


def categories(request):
    """ Return a list of categories to be inserted into the context dict by the context processor"""
    category_list = Category.objects.order_by('name')[:5]
    context_dict = {
        'categories': category_list,
    }
    return context_dict
