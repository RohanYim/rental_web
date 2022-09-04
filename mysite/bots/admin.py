from django.contrib import admin
from .models import FeaturesType, SystemType, Bot, BotSelling, Order, BotListing, BidOrder, ListOrder
# Register your models here.

@admin.register(FeaturesType)
class FeaturesTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)  # 后台显示的项目
    
@admin.register(SystemType)
class SystemTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)  # 后台显示的项目

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "twitter")  # 后台显示的项目

@admin.register(BotSelling)
class BotSelling(admin.ModelAdmin):
    list_display = ("cart_id","buyer_id")  # 后台显示的项目

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('user_id','order_number','status')  # 后台显示的项目

@admin.register(BidOrder)
class BidOrder(admin.ModelAdmin):
    list_display = ('bid_pk','seller_id','status')  # 后台显示的项目

@admin.register(ListOrder)
class ListOrder(admin.ModelAdmin):
    list_display = ('list_pk','buyer_id','status')  # 后台显示的项目
