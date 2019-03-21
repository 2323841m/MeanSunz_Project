from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # This line is required. Link UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name='profile')
    rating = models.IntegerField(default=0)

    picture = models.ImageField(upload_to='profile_image', blank=True)

    def __ste__(self):
        return self.user.username


class Category(models.Model):
    max_length = 128
    name = models.CharField(max_length=max_length, unique=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    picture = models.ImageField(upload_to='post_image', blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    content = models.CharField(max_length=1026, blank=False)
    picture = models.ImageField(upload_to='comment_image', blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.content
