from django.contrib import admin
from meansunz.models import Category, Post, UserProfile, Comment, VotePost, VoteComment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'upvotes', 'downvotes',)
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'user')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


class VotePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value')


class VoteCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'value')


admin.site.register(VoteComment, VoteCommentAdmin)
admin.site.register(VotePost, VotePostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
