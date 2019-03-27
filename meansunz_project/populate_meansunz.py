import datetime
import os
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meansunz_project.settings')

import django

django.setup()
from meansunz.models import Category, Post, User, UserProfile


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
                 "picture": ""},
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
         "picture": "",
         "user": get_random_user()}
    ]

    film_posts = [
        {"title": "Godfather",
         "description": "The best movie ever",
         "picture": "",
         "user": get_random_user()}
    ]

    music_posts = [
        {"title": "Rex Orange County",
         "description": "The best of the best",
         "picture": "",
         "user": get_random_user()}
    ]

    sport_posts = [
        {"title": "Aberdeen FC",
         "description": "Yes!",
         "picture": "",
         "user": get_random_user()}
    ]

    animation_posts = [
        {"title": "walking the dog",
         "description": "yoyo animation",
         "picture": "",
         "user": get_random_user()}
    ]

    categories = {
        "Gaming": {"Posts": gaming_posts,
                   },
        "Sport": {"Posts": sport_posts,
                  },
        "Music": {"Posts": music_posts,
                  },
        "Film": {"Posts": film_posts,
                 },
        "Animation": {"Posts": animation_posts,
                      },
    }

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated posts for that category.

    for cat, cat_data in categories.items():
        # views = cat_data.get("views", 0)
        # likes = cat_data.get("likes", 0)
        c = add_cat(cat)
        for p in cat_data["Posts"]:
            add_post(c, p["title"], p["user"], p["description"], p["picture"])

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
    p = Post.objects.get_or_create(category=cat, title=title, date=date, user=user)[0]
    p.description = description
    p.picture = picture
    p.upvotes = 0
    p.downvotes = 0
    p.save()
    return p


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("\nStarting Meansunz population script")
    populate()
