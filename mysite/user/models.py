from django.db import models
from django.contrib.auth.models import User
import datetime



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    discordname = models.CharField(max_length=20, default='')
    discordid = models.CharField(max_length=20, default='')
    discordavatar = models.CharField(max_length=200, default='')
    connected = models.BooleanField(default=False)
    timezone = models.CharField(max_length=15, choices=(('GMT+8','GMT+8'),('GMT-4','GMT-4'),('GMT+1','GMT+1')), default='GMT+8')

    def __str__(self):
        return '<Profile %s for %s>' % (self.discordname, self.user.username)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    sell_count = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    seller_fee = models.FloatField(default=20.0)
    warning = models.PositiveIntegerField(default=0)
    twitter_link = models.CharField(max_length=200, default='')
    Refs = models.PositiveIntegerField(default=0)

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    buy_count = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    points = models.FloatField(default=0.0)
    buyer_fee = models.FloatField(default=10.0)

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    total = models.FloatField(default=0.0)
    withdraw_able = models.FloatField(default=0.0)
    freeze = models.FloatField(default=0.0)
    points = models.FloatField(default=0.0)
    alipay_id = models.CharField(max_length=30,default='')

class BotInventory(models.Model):
    bots = (('Dashe','Dashe'),('Cyber','Cyber'),('Balko','Balko'))
    status_name = (('Processing Verification','Processing Verification'),('Ready to be listed','Ready to be listed'),('Not Verified','Not Verified'),('Listed','Listed'))
    user_id = models.CharField(max_length=20, default='')
    user_discord = models.CharField(max_length=30, default='')
    bot = models.CharField(max_length=15, choices=bots, default='')
    key = models.CharField(max_length=500, default='')
    key_nickname = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=30, choices=status_name, default='Processing Verification')
    img_url = models.CharField(max_length=100, default='')
    need_reset = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user_discord','key')

class Verify(models.Model):
    user_id = models.CharField(max_length=20, default='')
    user_discord = models.CharField(max_length=30, default='')
    bot = models.CharField(max_length=15, default='')
    key = models.CharField(max_length=200, default='')
    key_nickname = models.CharField(max_length=20, default='')
    status_name = (('Processing Verification','Processing Verification'),('Ready to be listed','Ready to be listed'),('Not Verified','Not Verified'),('Listed','Listed'))
    status = models.CharField(max_length=30, choices=status_name, default='Processing Verification')
    need_reset = models.BooleanField(default=False)


class Event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return self.name

class Rental(models.Model):
    keyreset = (('Waiting for reset','Waiting for reset'),('Nothing','Nothing'))
    rental = (('Active','Active'),('Upcoming','Upcoming'),('Past','Past'))
    way = (('Normal','Normal'),('Bid','Bid'))
    rental_from = models.CharField(max_length=30, choices=way, default='')
    buyer_id = models.CharField(max_length=20, default='')
    seller_id = models.CharField(max_length=20, default='')
    listing_num = models.PositiveIntegerField(default=0)
    bidding_num = models.PositiveIntegerField(default=0)
    keyreset_status = models.CharField(max_length=30, choices=keyreset, default='Nothing')
    rental_status = models.CharField(max_length=30, choices=rental, default='')
    keyreset_time = models.DateTimeField(default=datetime.datetime.now())
    request_time = models.CharField(max_length=200,default=datetime.datetime.now())

class Transaction(models.Model):
    statuses = (('Paid','Paid'),('Processing','Processing'),('Failed','Failed'))
    # time = models.DateTimeField(default=datetime.datetime.now())
    uses = (('topup','topup'),('withdrawal','withdrawal'),('Refund','Refund'))
    user = models.CharField(max_length=20, default='')
    amount = models.FloatField(default=0.0)
    use = models.CharField(max_length=20, choices=uses, default='')
    status = models.CharField(max_length=20, choices=statuses, default='')
    alipay_no = models.CharField(max_length=30,default='')
    alipay_id = models.CharField(max_length=30,default='')







