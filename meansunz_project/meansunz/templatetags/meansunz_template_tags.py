from django import template

register = template.Library()

@register.filter
def sub(val1, val2):
    return val1 - val2

@register.simple_tag
def get_user_rating(profile=None):
    return profile.rating_comment + profile.rating_post

@register.simple_tag
def get_post_votes(post=None):
    return post.upvotes - post.downvotes

@register.simple_tag
def get_comment_votes(comment=None):
    return comment.upvotes - comment.downvotes
