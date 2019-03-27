import datetime

from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_save
from django.utils import timezone


class UserProfile(models.Model):
    # This line is required. Link UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE,)
    picture = models.ImageField(upload_to='profile_image', blank=True)
    rating_comment = models.IntegerField(default=0)
    rating_post = models.IntegerField(default=0)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True)
    picture = models.ImageField(upload_to='post_image', blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    slug = models.SlugField()
    date = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    content = models.CharField(max_length=1026, blank=False)
    picture = models.ImageField(upload_to='comment_image', blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class VotePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "post")


class VoteComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "comment")


def update_votes(sender, instance, created, **kwargs):
    # update rating when a vote is updated
    with transaction.atomic():
        post = Post.objects.get(pk=instance.post_id)
        post.upvotes = post.votepost_set.filter(value=1).count()
        post.downvotes = post.votepost_set.filter(value=-1).count()
        post.save()

        # update user rating
        user = UserProfile.objects.get(user=instance.user)
        user_upvotes = Post.objects.filter(user=post.user).aggregate(Sum('upvotes'))['upvotes__sum']
        user_downvotes = Post.objects.filter(user=post.user).aggregate(Sum('downvotes'))['downvotes__sum']
        user.rating_post = user_upvotes - user_downvotes
        user.save()


post_save.connect(update_votes, sender=VotePost)


def update_votes_comments(sender, instance, created, **kwargs):
    # Update rating whenever a vote is updated
    with transaction.atomic():
        comment = Comment.objects.get(pk=instance.comment_id)
        comment.upvotes = comment.votecomment_set.filter(value=1).count()
        comment.downvotes = comment.votecomment_set.filter(value=-1).count()
        comment.save()

        # update user rating
        user = UserProfile.objects.get(user=instance.user)
        user_upvotes = Comment.objects.filter(user=comment.user).aggregate(Sum('upvotes'))['upvotes__sum']
        user_downvotes = Comment.objects.filter(user=comment.user).aggregate(Sum('downvotes'))['downvotes__sum']
        user.rating_comment = user_upvotes - user_downvotes
        user.save()


post_save.connect(update_votes_comments, sender=VoteComment)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Auto generate userprofile for superuser accounts
        if instance.is_superuser:
            UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
