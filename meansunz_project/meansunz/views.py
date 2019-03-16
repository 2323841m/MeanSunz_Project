from django.shortcuts import render
from meansunz.models import Category, Post
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    category_list = Category.objects.order_by('name')[:5]
    post_list = Post.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'posts': post_list, }

    response = render(request, 'meansunz/index.html', context_dict)
    return response


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        pages = Post.objects.filter(category=category)

        # Add our results list to the template context under name pages
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    get_categories(context_dict)

    # Go render the response and return it to the client.
    return render(request, 'meansunz/category.html', context_dict)


def get_categories(context_dict):
    """ Add categories to context dict to be displayed in nav bar """
    category_list = Category.objects.order_by('name')[:5]
    post_list = Post.objects.order_by('-views')[:5]
    context_dict['categories'] = category_list
    context_dict['posts'] = post_list
    return context_dict


def about(request):
    context_dict = {}
    get_categories(context_dict)
    response = render(request, 'meansunz/about.html', context_dict)
    return response


def leaderboards(request):
    context_dict = {}
    get_categories(context_dict)
    response = render(request, 'meansunz/leaderboards.html', context_dict)
    return response


def login(request):
    context_dict = {}
    response = render(request, 'meansunz/login.html', context_dict)
    return response


def register(request):
    context_dict = {}
    response = render(request, 'meansunz/register.html', context_dict)
    return response


def signout(request):
    context_dict = {}
    response = render(request, 'meansunz/signout.html', context_dict)
    return response


def myposts(request):
    context_dict = {}
    response = render(request, 'meansunz/myposts.html', context_dict)
    return response
