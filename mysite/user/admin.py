from django.contrib import admin
from .models import Profile, Seller, Buyer, Wallet, BotInventory, Verify, Rental, Transaction
from bots.models import BotListing, BotBidding
from django.db import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
class SellerInline(admin.StackedInline):
    model = Seller
    can_delete = False
class BuyerInline(admin.StackedInline):
    model = Buyer
    can_delete = False
class WalletInline(admin.StackedInline):
    model = Wallet
    can_delete = False
    

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,SellerInline,BuyerInline,WalletInline)
    list_display = ('username', 'discordname', 'discordid', 'connected', 'timezone', 'is_staff','is_active', 'is_superuser')

    def discordname(self, obj):
        return obj.profile.discordname
    def discordid(self, obj):
        return obj.profile.discordid
    def connected(self, obj):
        return obj.profile.connected
    def timezone(self, obj):
        return obj.profile.timezone
    def sell_count(self, obj):
        return obj.seller.sell_count
    def level(self, obj):
        return obj.seller.level
    def seller_fee(self, obj):
        return obj.seller.seller_fee
    def warning(self, obj):
        return obj.seller. warning

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'discordname', 'discordid','connected','timezone')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'sell_count', 'level', 'warning')

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'buy_count', 'points')

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'withdraw_able', 'freeze', 'points')

@admin.register(BotInventory)
class BotInventoryAdmin(admin.ModelAdmin):
    list_display = ("user_id","user_discord", "bot", "key","status")  # 后台显示的项目
    
@admin.register(Verify)
class VerifyAdmin(admin.ModelAdmin):
    list_display = ("user_id","user_discord", "bot", "key", "status")  # 后台显示的项目

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("seller_id","buyer_id","listing_num", "keyreset_status", "rental_status")  # 后台显示的项目


@admin.register(BotListing)
class BotListingAdmin(admin.ModelAdmin):
    list_display = ("user", "bot", "key", "listing_type","start_time","end_time")  # 后台显示的项目

@admin.register(BotBidding)
class BotBiddingAdmin(admin.ModelAdmin):
    list_display = ("user", "bot", "listing_type","start_time","end_time")  # 后台显示的项目

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount","use","status")  # 后台显示的项目