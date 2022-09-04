from django.contrib import admin
from .models import ItemInCart
# Register your models here.

@admin.register(ItemInCart)
class ItemInCartAdmin(admin.ModelAdmin):
    list_display = ("pk",)  # 后台显示的项目