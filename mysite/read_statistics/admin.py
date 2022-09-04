from django.contrib import admin
from .models import ReadCount, ReadDetail

# Register your models here.
@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    list_display = ("read_count", "content_object")  # 后台显示的项目

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ("date", "read_count", "content_object")  # 后台显示的项目