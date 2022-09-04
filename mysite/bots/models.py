from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime

# Create your models here.
class FeaturesType(models.Model):
    name = models.CharField(max_length=15, default='')
    def __str__(self):
        return self.name

class SystemType(models.Model):
    name = models.CharField(max_length=15, default='')
    def __str__(self):
        return self.name

class Bot(models.Model):
    name = models.CharField(max_length=15, default='')
    website = models.CharField(max_length=100, default='')
    twitter = models.CharField(max_length=100, default='')
    features = models.ManyToManyField("FeaturesType")
    systems = models.ManyToManyField("SystemType")
    img_url = models.CharField(max_length=100, default='')
    def __str__(self):
        return self.name

class BotListing(models.Model):
    status = (('Show','Show'),('Unshow','Unshow'))
    keyreset = (('Waiting for reset','Waiting for reset'),('Nothing','Nothing'))
    user = models.CharField(max_length=25, default='')
    user_timezone = models.CharField(max_length=25, default='')
    user_level = models.PositiveIntegerField(default=0)
    user_sellingnum = models.PositiveIntegerField(default=0)
    user_refs = models.PositiveIntegerField(default=0)
    bot = models.CharField(max_length=25, default='')
    img_url = models.CharField(max_length=100, default='')
    key = models.CharField(max_length=500, default='')
    key_nickname = models.CharField(max_length=200, default='')
    listing_type = models.CharField(max_length=30, default='')
    start_time = models.CharField(max_length=200, default='')
    end_time =models.CharField(max_length=200, default='')
    rmb_price = models.FloatField(default=0.0)
    usd_price = models.FloatField(default=0.0)
    status = models.CharField(max_length=15, choices=status, default='Show')
    keyreset_status = models.CharField(max_length=30, choices=keyreset, default='Nothing')
    keyreset_time = models.DateTimeField(default=datetime.datetime.now())
    request_time = models.CharField(max_length=200,default=datetime.datetime.now())

class BotBidding(models.Model):
    status = (('Show','Show'),('Unshow','Unshow'))
    payment_status = (('Listing','Listing'),('Unpaid','Unpaid'),('Paid','Paid'))
    keyreset = (('Waiting for reset','Waiting for reset'),('Nothing','Nothing'))
    user = models.CharField(max_length=25, default='')
    bot = models.CharField(max_length=25, default='')
    img_url = models.CharField(max_length=100, default='')
    listing_type = models.CharField(max_length=30, default='')
    start_time = models.CharField(max_length=200, default='')
    end_time =models.CharField(max_length=200, default='')
    rmb_price = models.FloatField(default=0.0)
    usd_price = models.FloatField(default=0.0)
    key = models.CharField(max_length=200, default='', null=True)
    key_nickname = models.CharField(max_length=200, default='', null=True)
    status = models.CharField(max_length=15, choices=status, default='Show')
    payment_status = models.CharField(max_length=15, choices=payment_status, default='Listing')
    order_time = models.DateTimeField(default=datetime.datetime.now())
    remove_time = models.DateTimeField(default=datetime.datetime.now())
    keyreset_status = models.CharField(max_length=30, choices=keyreset, default='Nothing')
    keyreset_time = models.DateTimeField(default=datetime.datetime.now())
    request_time = models.CharField(max_length=200,default=datetime.datetime.now())

class BotSelling(models.Model):
    cart_id = models.CharField(max_length=30, default='')
    buyer_id = models.CharField(max_length=30, default='')

class Order(models.Model):
    status = (('Created','Created'),('Paid','Paid'))
    user_id = models.CharField(max_length=30, default='')
    order_number = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=15, choices=status, default='Created')

class BidOrder(models.Model):
    status = (('Unpaid','Unpaid'),('Paid','Paid'),('Processing','Processing'))
    bid_pk = models.ForeignKey(BotBidding, on_delete=models.DO_NOTHING)
    seller_id = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=15, choices=status, default='Unpaid')
    key = models.CharField(max_length=200, default='')
    key_nickname = models.CharField(max_length=200, default='')
    order_time = models.DateTimeField(default=datetime.datetime.now())
    remove_time = models.DateTimeField(default=datetime.datetime.now())
    alipay_no = models.CharField(max_length=30, default='')

class ListOrder(models.Model):
    status = (('Unpaid','Unpaid'),('Paid','Paid'))
    list_pk = models.ForeignKey(BotListing, on_delete=models.DO_NOTHING)
    buyer_id = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=15, choices=status, default='Unpaid')
    points = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    alipay_no = models.CharField(max_length=30, default='')