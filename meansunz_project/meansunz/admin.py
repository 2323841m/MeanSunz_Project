from django.contrib import admin
from meansunz.models import Category, Post, UserProfile


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'likes')


admin.site.register(UserProfile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
