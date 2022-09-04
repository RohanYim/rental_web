from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from bots.models import BotBidding, BidOrder, BotListing
from django.contrib.auth.models import User
from user.models import Rental,Buyer,Seller
from cart.models import ItemInCart
import datetime
from mysite.compare_time import compare_time
import pytz
from pythonProject.command_field import command_field
import configparser
import os

# 实例化调度器
scheduler = BackgroundScheduler()
# 调度器使用默认的DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), 'default')

# 每10秒执行一次检查
@register_job(scheduler, "interval", seconds=10)
def order_expire():
    bidding = BotBidding.objects.all()
    # 检查bidding是否过期
    for i in bidding:
        time_compare, listing_delete = compare_time(i.start_time,i.end_time)
        if listing_delete:
            i.delete()
        # 如果bidding到时未支付，删除该bidding，删除相应bid order中的数据
        now = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        if now > i.remove_time and i.payment_status == 'Unpaid':
            order = BidOrder.objects.get(bid_pk=i)
            order.delete()
            i.delete()
    # 检查listing是否过期
    botlisting = BotListing.objects.filter(status='Show')
    for i in botlisting:
        time_compare, listing_delete = compare_time(i.start_time,i.end_time)
        if listing_delete:
            i.delete()
    # 检查rental的状态
    for i in Rental.objects.filter(rental_status='Upcoming'):
        if i.rental_from == 'Normal':
            time_compare, listing_delete = compare_time(BotListing.objects.get(pk=i.listing_num).start_time, BotListing.objects.get(pk=i.listing_num).end_time)
            if time_compare:
                i.rental_status = 'Active'
                i.save()
                # 给买家卖家发送dc message
                order_number = '1'+'#'+ str(i.listing_num)
                print('sending...')
                command_field(order_number, 'start_seller','order')
                command_field(order_number, 'start_buyer','order')
        if i.rental_from == 'Bid':
            time_compare, listing_delete = compare_time(BotBidding.objects.get(pk=i.bidding_num).start_time, BotBidding.objects.get(pk=i.bidding_num).end_time)
            if time_compare:
                i.rental_status = 'Active'
                i.save()
                # 给买家卖家发送dc message
                order_number = '2'+'#'+ str(i.bidding_num)
                command_field(order_number, 'start_seller','order')
                command_field(order_number, 'start_buyer','order')

    for i in Rental.objects.filter(rental_status='Active'):
        if i.rental_from == 'Normal':
            time_compare, listing_delete = compare_time(BotListing.objects.get(pk=i.listing_num).start_time, BotListing.objects.get(pk=i.listing_num).end_time)
            if not time_compare:
                i.rental_status = 'Past'
                i.save()
                # 给买家卖家发送dc message
                order_number = '1'+'#'+ str(i.listing_num)
                command_field(order_number, 'end_seller','order')
                command_field(order_number, 'end_buyer','order')
        if i.rental_from == 'Bid':
            time_compare, listing_delete = compare_time(BotBidding.objects.get(pk=i.bidding_num).start_time, BotBidding.objects.get(pk=i.bidding_num).end_time)
            if not time_compare:
                i.rental_status = 'Past'
                i.save()
                # 给买家卖家发送dc message
                order_number = '2'+'#'+ str(i.bidding_num)
                command_field(order_number, 'end_seller','order')
                command_field(order_number, 'end_buyer','order')
    # 检查购物车中是否有unshow的bid和list
    cart = ItemInCart.objects.all()
    for j in cart:
        for i in j.bidding.all():
            if i.status == 'Unshow':
                j.bidding.remove(i)
        for i in j.listing.all():
            if i.status == 'Unshow':
                j.listing.remove(i)

@register_job(scheduler, "interval", seconds=30)
def user_level():
    seller = Seller.objects.all()
    for i in seller:
        if i.sell_count >= 20:
            i.level = 2
            i.seller_fee = 18.5
            i.save()
    buyer = Buyer.objects.all()
    for i in buyer:
        if i.buy_count >= 20:
            i.level = 2
            i.save()
    

# 注册定时任务并开始
register_events(scheduler)
scheduler.start()
