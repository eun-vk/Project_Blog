from django.contrib import admin
from .models import Profile
from blog.models import Post, Comment  # ✅ Comment는 blog.models에서 가져옴


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'views', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at']
