import datetime
import json

from django.shortcuts import render
from meansunz.models import Category, Post, UserProfile, User, Comment, VotePost, VoteComment
from meansunz.forms import CategoryForm, PostForm, UserForm, UserProfileForm, CommentForm, UserUpdateForm
from meansunz.decorators import ajax_login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.list import ListView


class index(ListView):
    model = Post
    # Amount of posts to render at a time
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'meansunz/index.html'

    # Query database
    def get_queryset(self, **kwargs):
        # Get posts by cat and order by the rating score and the chosen in sorting mode
        if self.request.GET.get('sort'):
            sort = self.request.GET.get('sort')
            posts = Post.objects.extra(select={'votes': 'upvotes - downvotes'}, order_by=('-' + sort,))
        else:
            posts = Post.objects.extra(select={'votes': 'upvotes - downvotes'}, order_by=('-votes',))

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None

        # Append user's vote to each post, if logged in
        post_list = append_votes(posts, user)

        return post_list

    def get_context_data(self, **kwargs):
        # Get context dict for show_post, get sort from the select box and category from the url parameter
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort')
        context['category'] = 'index'  # used to enable sort
        return context


class show_category(ListView):
    model = Post
    # Amount of posts to render at a time
    paginate_by = 1
    context_object_name = 'posts'
    template_name = 'meansunz/category.html'

    # Query database
    def get_queryset(self, **kwargs):
        try:
            # Get category by slug
            category = Category.objects.get(slug=self.kwargs['category_name_slug'])
        except Category.DoesNotExist:
            category = None

        # Get posts by cat and order by the rating score and the chosen in sorting mode
        if self.request.GET.get('sort'):
            sort = self.request.GET.get('sort')
            posts = Post.objects.filter(category=category).extra(select={'votes': 'upvotes - downvotes'},
                                                                 order_by=('-' + sort,))
        else:
            posts = Post.objects.filter(category=category).extra(select={'votes': 'upvotes - downvotes'},
                                                                 order_by=('-votes',))

        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None

        # Append user's vote to each post, if logged in
        post_list = append_votes(posts, user)
        return post_list

    def get_context_data(self, **kwargs):
        # Get context dict for show_post, get sort from the select box and category from the url parameter
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort')
        try:
            cat = Category.objects.get(slug=self.kwargs['category_name_slug'])
            context['category'] = cat
        except Category.DoesNotExist:
            context['category'] = None
        return context


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        if Category.objects.all().count() >= 10:
            return HttpResponse(
                "Only 10 categories can be made if you want to add a new category please remove an existing one")
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
        user = request.user
    except User.DoesNotExist:
        return HttpResponse("No user")
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if category:
                post = form.save(commit=False)
                if 'picture' in request.FILES:
                    post.picture = form.cleaned_data['picture']
                post.category = category
                post.user = user
                post.views = 0
                post.date = datetime.datetime.now()
                post.save()
                return redirect("show_category", category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'meansunz/create_post.html', context_dict)


def show_post(request, category_name_slug, post_id, post_title_slug):
    context_dict = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
        post = Post.objects.get(id=post_id, slug=post_title_slug, category=cat)
        category = Category.objects.get(slug=category_name_slug)
        comments = Comment.objects.filter(post=post).order_by('-upvotes')

        # Get user if authenticated, used to check if user has liked post
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

    # If user tries to access a post that doesn't exist redirect them back to index
    except Post.DoesNotExist:
        return redirect(reverse('index'))
    except Category.DoesNotExist:
        return redirect(reverse('index'))

    # Append user's vote to each comment, if logged in
    comment_list = []
    for comment in comments:
        comment_list.append((comment, VoteComment.objects.filter(user=user, comment=comment)))

    context_dict['comments'] = comment_list
    context_dict['category'] = category
    # tells render_post if user has voted on this post
    context_dict['posts'] = [(post, VotePost.objects.filter(user=user, post=post))]
    context_dict['post'] = post

    # read comment form input
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            if post:
                comment = form.save(commit=False)

                if 'picture' in request.FILES:
                    comment.picture = form.cleaned_data['picture']

                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect(show_post, category_name_slug, post_id, post_title_slug)
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'meansunz/post.html', context_dict)


@ajax_login_required
def vote_comment(request, category_name_slug, post_id, post_title_slug):
    if request.method == 'POST':
        value = request.POST.get('vote', 0)
        try:
            comment = Comment.objects.get(id=request.POST.get('id'))
            vote = VoteComment.objects.get(user=request.user, comment=comment)
            # if user has already voted this way
            if int(vote.value) == int(value):
                # cancel vote
                vote.value = 0
                value = 0
            else:
                vote.value = value
            vote.save()
        except VoteComment.DoesNotExist:
            # if user hasn't voted yet create a new vote
            vote = VoteComment.objects.create(user=request.user, comment=comment, value=value)
            vote.save()

    comment = Comment.objects.get(id=request.POST.get('id'))  # get updated comment
    jsonr = json.dumps({'rating': (comment.upvotes - comment.downvotes), 'voted': value})
    return HttpResponse(jsonr, content_type='application/json')  # respond with new rating score and users vote


@ajax_login_required
def vote(request, category_name_slug, post_id, post_title_slug):
    if request.method == 'POST':
        value = request.POST.get('vote', 0)
        try:
            post = Post.objects.get(id=post_id)
            vote = VotePost.objects.get(user=request.user, post=post)
            if int(vote.value) == int(value):
                vote.value = 0
                value = 0
            else:
                vote.value = value
            vote.save()
        except VotePost.DoesNotExist:
            vote = VotePost.objects.create(user=request.user, post=post, value=value)
            vote.save()

    post = Post.objects.get(id=post_id)  # Get updated post
    jsonr = json.dumps({'rating': (post.upvotes - post.downvotes), 'voted': value})
    return HttpResponse(jsonr, content_type='application/json')  # respond with new rating score and users vote


def about(request):
    context_dict = {}
    response = render(request, 'meansunz/about.html', context_dict)
    return response


def leaderboards(request):
    context_dict = {}
    user_ranking = UserProfile.objects.extra(select={'votes': 'rating_comment + rating_post'}, order_by=('-votes',))[
                   :15]
    context_dict['profiles'] = user_ranking
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
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details
            print("Invalid login details {0}, {1}".format(username, password))
            message = 'Your login details are invalid'
            return render(request, 'meansunz/login.html', {'message': message})

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
    posts = Post.objects.filter(user=request.user).order_by('-date',)

    post_list = append_votes(posts, request.user)

    context_dict = {'posts': post_list}
    response = render(request, 'meansunz/user_posts.html', context_dict)
    return response


@login_required
def user_profile(request):
    posts = Post.objects.filter(user=request.user).order_by('-date')[:3]
    post_list = append_votes(posts, request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.get(id=request.user.id)
            # Hash password with set_password method
            user.set_password(user_form.data.get('password'))
            user.email = (user_form.data.get('email'))
            user.save()
            profile = UserProfile.objects.get(user=user)

            # Did the user provide a profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

        else:
            # Invalid form, mistakes, or something else
            print(user_form.errors, profile_form.errors)
    else:
        # Not an HTTP POST, so render form using two ModelForm instances
        # These forms will be blank, ready for user input
        user_form = UserUpdateForm()
        profile_form = UserProfileForm()

    context_dict = {'user': request.user, 'posts': post_list, 'form': profile_form, 'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'meansunz/user_profile.html', context_dict)


# Helper function
def append_votes(posts, user):
    # Append user's votes to posts
    post_list = []
    for post in posts:
        post_list.append((post, VotePost.objects.filter(user=user, post=post)))
    return post_list
