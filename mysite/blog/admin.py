from django.contrib import admin
from .models import Blog, BlogType


# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name")  # 后台显示的项目
    ordering = ("id",)  # 排序规则,"-id"为倒序



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "blog_type", "author","get_read_count", "create_time", "last_update_time")  # 后台显示的项目
    ordering = ("id",)  # 排序规则,"-id"为倒序


