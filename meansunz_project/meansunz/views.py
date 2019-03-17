from django.shortcuts import render
from meansunz.models import Category, Post, UserProfile, User, Comment
from meansunz.forms import CategoryForm, PostForm, UserForm, UserProfileForm, CommentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def index(request):
    post_list = Post.objects.order_by('-views')[:25]
    context_dict = {'posts': post_list, }

    response = render(request, 'meansunz/index.html', context_dict)
    return response


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        posts = Post.objects.filter(category=category).order_by('-likes')

        context_dict['posts'] = posts
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['posts'] = None

    return render(request, 'meansunz/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print(form.errors)

    return render(request, 'meansunz/add_category.html', {'form': form})


@login_required
def create_post(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    try:
        user = request.user.profile
    except UserProfile.DoesNotExist:
        return HttpResponse(
            "User has no profile")  # TODO: Force creation of UserProfile whenever a new user object is created

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(data=request.POST)

        if form.is_valid():
            if category:
                post = form.save(commit=False)
                if 'picture' in request.FILES:
                    post.picture = request.FILES['picture']
                post.category = category
                post.user = user
                post.views = 0
                post.save()
                return redirect(show_category, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'meansunz/create_post.html', context_dict)


def show_post(request, category_name_slug, post_id, post_title_slug):
    context_dict = {}
    try:
        post = Post.objects.get(id=post_id)
        category = Category.objects.get(slug=category_name_slug)
        comments = Comment.objects.filter(post=post).order_by('-likes')

    except Post.DoesNotExist:
        post = None
        category = None
        comments = None
    except Category.DoesNotExist:
        post = None
        category = None

    context_dict['comments'] = comments
    context_dict['category'] = category
    context_dict['post'] = post

    # read comment form input
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(data=request.POST)

        if form.is_valid():
            if post:
                comment = form.save(commit=False)
                if 'picture' in request.FILES:
                    comment.picture = request.FILES['picture']
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect(show_post, category_name_slug, post_id, post_title_slug)
        else:
            print(form.errors)
    context_dict['form'] = form

    return render(request, 'meansunz/post.html', context_dict)


@login_required
def vote_comment(request, category_name_slug, post_id, post_title_slug):
    if request.method == 'POST':
        if 'upvote_comment' in request.POST:
            comment = Comment.objects.get(id=request.POST.get('id', None))
            comment.likes += 1
            comment.save()

        elif 'downvote_comment' in request.POST:
            comment = Comment.objects.get(id=request.POST.get('id', None))
            comment.likes -= 1
            comment.save()

        return redirect(show_post, category_name_slug, post_id, post_title_slug)


# TODO: implement voting system using script
@login_required
def vote(request, category_name_slug, post_id, post_title_slug):
    if request.method == 'POST':
        if 'upvote_post' in request.POST:
            post = Post.objects.get(id=post_id)
            post.likes += 1
            post.save()

        elif 'downvote_post' in request.POST:
            post = Post.objects.get(id=post_id)
            post.likes -= 1
            post.save()

        return redirect(request.POST.get('next', '/'), category_name_slug, post_id, post_title_slug)


def about(request):
    context_dict = {}
    response = render(request, 'meansunz/about.html', context_dict)
    return response


def leaderboards(request):
    context_dict = {}
    response = render(request, 'meansunz/leaderboards.html', context_dict)
    return response


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Check if account hasn't been disabled
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details
            print("Invalid login details {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'meansunz/login.html', {})


def register(request):
    # Boolean value for telling the template whether the registration was successful.
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Hash password with set_password method
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            # Invalid form, mistakes, or something else
            print(user_form.errors, profile_form.errors)
    else:
        # Not an HTTP POST, so render form using two ModelForm instances
        # These forms will be blank, ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, }
    return render(request, 'meansunz/register.html', context_dict)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def user_posts(request):
    posts = Post.objects.filter(user=request.user.profile)
    context_dict = {'posts': posts}
    response = render(request, 'meansunz/user_posts.html', context_dict)
    return response
