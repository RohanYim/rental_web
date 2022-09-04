from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content_object", "text", "comment_time", "user")  # 后台显示的项目
    ordering = ("id",)  # 排序规则,"-id"为倒序