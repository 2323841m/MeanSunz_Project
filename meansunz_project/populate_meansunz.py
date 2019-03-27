import os
import random

from django.core.files import File
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meansunz_project.settings')

import django

django.setup()
from meansunz.models import Category, Post, User, UserProfile,Comment


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category
    # Then we will create a dictionary of dictionaries for our categories
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models

    # Create users
    user_dict = {
        "Iain": {"email": "Iain@meansunz.com",
                 "password": "p4ssword",
                 "picture": ""},
        "Matthew": {"email": "Matthew@meansunz.com",
                    "password": "potato",
                    "picture": ""},
        "Peter": {"email": "Peter@meansunz.com",
                  "password": "dogdog",
                  "picture": ""},
        "Ewan": {"email": "Ewan@meansunz.com",
                 "password": "greenjacket",
                 "Picture":"meansunz_project/population/media_files/pic1.jpg"},

    }
    add_users(user_dict)
    add_superuser("admin", "admin@meansunz.com", "changeme")

    # Template
    blank_posts = [
        {"title": "",
         "description": "",
         "picture": "",
         "user": get_random_user()}
    ]

    gaming_posts = [
        {"title": "Games!",
         "description": "Hearthstone hacks",
         "picture": "meansunz_project/population/media_files/hstonehack.jpg",
         "user": get_random_user()},
        {"title": "Call Of Duty!",
         "description": "My thought is that call of duty is getting repetitive do you agree?",
         "picture": "meansunz_project/population/media_files/game.jpg",
         "user": get_random_user()}
    ]

    film_posts = [
        {"title": "Godfather",
         "description": "The best movie ever",
         "picture": "meansunz_project/population/media_files/The_Godfather_Don_Corleone.png",
         "user": get_random_user()}
    ]

    music_posts = [
        {"title": "Rex Orange County",
         "description": "The best of the best",
         "picture": "meansunz_project/population/media_files/rc.jpg",
         "user": get_random_user()}
    ]

    sport_posts = [
        {"title": "Scotland FC",
         "description": "Yes!",
         "picture": "meansunz_project/population/media_files/scot.jpg",
         "user": get_random_user()},
        {"title": "England FC",
         "description": "Yes!",
         "picture": "meansunz_project/population/media_files/eng.jpg",
         "user": get_random_user()},
        {"title": "Aberdeen FC",
         "description": "Yes!",
         "picture": "meansunz_project/population/media_files/ad.jpg",
         "user": get_random_user()}
    ]

    pets_posts = [
        {"title": "walking the dog",
         "description": "my dog",
         "picture": "meansunz_project/population/media_files/cute-dog (13).jpg",
         "user": get_random_user()},
        {"title": "My dog is better than yours",
         "description": "meet coco",
         "picture": "meansunz_project/population/media_files/cute-puppies-puppies-and-more-31104113-1024-768.jpg",
         "user": get_random_user()}
    ]

    gaming_comments = [
        {"post": "Games!",
         "content": "I played that",
         "picture": "meansunz_project/population/media_files/pic5.jpg",
         "user": get_random_user()},
        {"post": "Call Of Duty!",
         "content": "No I Do Not",
         "picture": "meansunz_project/population/media_files/angry.jpg",
         "user": get_random_user()}

    ]

    film_comments = [

    ]

    music_comments = [
        {"post": "Rex Orange County",
         "content": """I attached the lyrics to verse 1 of paradise:Don’t miss me when I’m dead
Live life and don’t think twice
Don’t miss me when I’m gone
I’ll see you soon in paradise
When I leave you
Take my last few pennies
And buy yourself something nice
Because, before you know it
We’ll be together again """,
         "picture": "",
         "user": get_random_user()}
    ]

    sport_comments = [

    ]

    pets_comments = [
        {"post": "My dog is better than yours",
         "content": "No it is not! why would you say something you know is a lie",
         "picture": "meansunz_project/population/media_files/dog.jpg",
         "user": get_random_user()},
        {"post": "My dog is better than yours",
         "content": "I agree with the poster",
         "picture": "meansunz_project/population/media_files/dog2.jpg",
         "user": get_random_user()}
    ]

    categories = {
        "Gaming": {"Posts": gaming_posts,"Comments":gaming_comments,
                   },
        "Sport": {"Posts": sport_posts,"Comments":sport_comments,
                  },
        "Music": {"Posts": music_posts,"Comments":music_comments,
                  },
        "Film": {"Posts": film_posts,"Comments":film_comments,
                 },
        "Pets": {"Posts": pets_posts,"Comments":pets_comments,
                      },
    }

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated posts for that category.

    for cat, cat_data in categories.items():
        # views = cat_data.get("views", 0)
        # likes = cat_data.get("likes", 0)
        c = add_cat(cat)
        print(c)
        for p in cat_data["Posts"]:
            n=add_post(c, p["title"], p["user"], p["description"], p["picture"])
            for comment in cat_data["Comments"]:
                try:
                    newpost = n[0]
                except TypeError:
                    newpost = n
                print(newpost)
                add_comment(newpost,comment["user"],comment["content"],comment["picture"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        print("\nCategory - " + str(c))
        print("Posts:")
        for p in Post.objects.filter(category=c):
            print("- {0}".format(str(p)))

    print("\nUsers: ")
    for u in User.objects.all():
        print(u.username)

    print("\nFinished populating database\n")


def add_users(user_dict):
    for user, user_data in user_dict.items():
        email = user_data.get("email")
        password = user_data.get("password")
        picture = user_data.get("picture")
        u = User.objects.filter(username=user)
        if not u:
            u = User.objects.create_user(username=user, password=password, email=email)
            UserProfile.objects.create(user=u, picture=picture)


def add_superuser(username, email, password):
    if not User.objects.filter(username=username):
        User.objects.create_superuser(username, email, password)


def get_random_user():
    users = User.objects.all()
    return random.choice(users)


def add_post(cat, title, user, description="", picture=""):
    date = timezone.now()
    p = Post.objects.filter(category=cat, title=title)
    if not p:
        p = Post.objects.create(category=cat, date=date, title=title, user=user)
        if picture:
            # Open the picture as a django file so that it is uploaded to media
            f = open(picture, "rb")
            p.picture = File(f)
        p.description = description
        p.upvotes = 0
        p.downvotes = 0
        p.save()
    return p


def add_comment(post, user, content="", picture=""):
    c = Comment.objects.filter(post=post, content=content, user=user)
    if not c:
        c = Comment.objects.create(post=post, content=content, user=user)
    if picture:
        # Open the picture as a django file so that it is uploaded to media
        f = open(picture, "rb")
        c.picture = File(f)
    c.upvotes = 0
    c.downvotes = 0
    c.save()
    return c


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("\nStarting Meansunz population script")
    populate()
