from django.shortcuts import render
from meansunz.models import Category, Post
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):

    #category_list = Category.objects.order_by('title')[:5]
    #page_list = Post.objects.order_by('-views')[:5]
    #context_dict = {'categories': category_list, 'pages': page_list, }
    context_dict = {}
    response = render(request, 'meansunz/index.html', context_dict)
    return response

def about(request):

    context_dict = {}
    response = render(request, 'meansunz/about.html', context_dict)
    return response

def leaderboards(request):

    context_dict = {}
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