import datetime
import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meansunz_project.settings')

import django

django.setup()
from meansunz.models import Category, Post, User


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category
    # Then we will create a dictionary of dictionaries for our categories
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models

    # Create users
    user_dict = {
        "Iain": {"email": "Iain@meansunz.com",
                 "password": "changeme"},
        "Matthew": {"email": "Matthew@meansunz.com",
                    "Password": "changeme"},
        "Peter": {"email": "Peter@meansunz.com",
                  "Password": "changeme"},
        "Ewan": {"email": "Ewan@meansunz.com",
                 "Password": "changeme"},
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
         "description": "",
         "picture": "",
         "user": get_random_user()}
    ]

    film_posts = [
        {"title": "Hello",
         "description": "Testing",
         "picture": "",
         "user": get_random_user()}
    ]

    categories = {
        "Gaming": {"Posts": gaming_posts,
                   },
        "Sport": {"Posts": "",
                  },
        "Music": {"Posts": "",
                  },
        "Film": {"Posts": film_posts,
                 },
        "Animation": {"Posts": "",
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
        for p in Post.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

    for u in User.objects.all():
        print(u.username)


def add_users(user_dict):
    for user, user_data in user_dict.items():
        email = user_data.get("email")
        password = user_data.get("password")
        u = User.objects.filter(username=user)
        if not u:
            User.objects.create_user(username=user, password=password, email=email)

def add_superuser(username, email, password):
    if not User.objects.filter(username=username):
        User.objects.create_superuser(username, email, password)


def get_random_user():
    users = User.objects.all()
    return random.choice(users)


def add_post(cat, title, user, description="", picture=""):
    date = datetime.datetime.now()
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
    print("Starting Rango population script")
    populate()
