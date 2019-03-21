from django.contrib import admin
from meansunz.models import Category, Post, UserProfile, Comment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'likes',)
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'user')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
