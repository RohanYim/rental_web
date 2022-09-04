from .models import ItemInCart
from user.models import Buyer, Wallet, Seller
from django.shortcuts import render,redirect
from bots.models import Bot, BotListing, Order, BotSelling, BotBidding, BidOrder, ListOrder
from user.models import Buyer, Wallet, Rental, BotInventory
from django.contrib.auth.models import User
import time
from urllib.parse import parse_qs
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .alipay import AliPay
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
from mysite.compare_time import compare_time, compare_time_when_listing
import pytz
from collections import Counter
from pythonProject.command_field import command_field
import configparser
import os

# Create your views here.
def aliPay():
    obj = AliPay(
        appid="2021000118614830",                              # 支付宝沙箱里面的APPID，需要改成你自己的
        app_notify_url='http://localhost:8000/cart/check_order/',  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        return_url="http://localhost:8000/cart/result/",            # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
        alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
        app_private_key_path=settings.APP_PRIVATE,      # 应用私钥
        debug=True,  # 默认False,True表示使用沙箱环境测试
    )
    return obj


def cart(request):
    try:
        cart = ItemInCart.objects.get(user=request.user)
    except:
        cart = ''
    wallet = Wallet.objects.get(user=request.user)
    keys_list = {}

    # 检查key的可用性
    for i in cart.bidding.all():
        bot = i.bot
        start_time = i.start_time
        end_time = i.end_time
        keys = BotInventory.objects.filter(user_id=request.user.username,bot=bot,status='Ready to be listed')
        # 遍历botlisting表和bidorder表
        temp = []
        for j in keys:
            flag = True
            check_time = BotListing.objects.filter(user=request.user.username,bot=bot,key=j.key,status='Unshow')
            for k in check_time:
                result = compare_time_when_listing(k.start_time,start_time,k.end_time,end_time)
                if result == False:
                    flag = False
                    continue
            check_time = BidOrder.objects.filter(seller_id=request.user.username,key=j.key,status='Paid')
            for k in check_time:
                result = compare_time_when_listing(k.bid_pk.start_time,start_time,k.bid_pk.end_time,end_time)
                if result == False:
                    flag = False
                    continue
            if flag == True:
                temp.append(j.key)
        keys_list[i.pk] = temp

    context = {
        'cart': cart,
        'wallet': wallet,
        'keys_list':keys_list,
    }
    if request.POST.get('flag') == 'delete_cart':
        listing_pk = request.POST.get('pk')
        cart = ItemInCart.objects.get(user_id=request.user, payment_status="Created")
        listing = BotListing.objects.get(pk=listing_pk)
        cart.listing.remove(listing)
        data = {}
        data['success'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'order':
        # 实例化SDK里面的类AliPay
        alipay = aliPay()

        # 对购买的数据进行加密
        money = float(request.POST.get('price'))  # 保留俩位小数  前端传回的数据
        listing = request.POST.get('listing')
        points = request.POST.get('use_points')
        balance = request.POST.get('use_balance')

        # 1. 在数据库创建一条数据：状态（待支付）
        cart = ItemInCart.objects.get(user=request.user)
    
        subject = ''
        for i in cart.listing.all():
            # 给每个listing创建一个order表，状态为unpaid
            # 如果之前有未支付的订单，删除之前的订单
            try:
                check = ListOrder.objects.filter(list_pk=i,buyer_id=request.user.username,status='Unpaid')
                for j in check:
                    j.delete()
            except:
                pass

            list_order = ListOrder.objects.create(list_pk=i,buyer_id=request.user.username,status='Unpaid',points=points,balance=balance)
            subject += str(i.pk)
        now = datetime.datetime.now()
        now_str = now.strftime('%Y%m%d%H%M%S')
        out_trade_no = now_str + '1' + str(subject)
        # 给每个listing order添加订单号
        for i in cart.listing.all():
            list_order = ListOrder.objects.get(list_pk=i,buyer_id=request.user.username,status='Unpaid',points=points,balance=balance)
            list_order.alipay_no = out_trade_no
            list_order.save()
        query_params = alipay.direct_pay(
            subject="Listing#" + str(subject),  # 商品简单描述 这里一般是从前端传过来的数据
            out_trade_no=out_trade_no,  # 商户订单号  这里一般是从前端传过来的数据
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
        )
        # 拼接url，转到支付宝支付页面
        pay_url = "https://openapi.alipaydev.com/gateway.do?"+query_params
        return JsonResponse(pay_url, safe=False)
    elif request.POST.get('flag') == 'check_success':
        alipay = aliPay()
        #获取订单号
        cart = ItemInCart.objects.get(user=request.user)
        for i in cart.listing.all():
            list_order = ListOrder.objects.get(list_pk=i,buyer_id=request.user.username,status='Unpaid')
            out_trade_no = list_order.alipay_no
        # 查询交易状态
        response = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        print(response)
        amount = float(response['alipay_trade_query_response']['total_amount'])
        data = {}
        if response['alipay_trade_query_response']['code'] == '40004':
                data['status'] = 'Payment is still processing!'
        if response['alipay_trade_query_response']['code'] == '10000':
            # 如果支付成功

            flag = True
            need_refund = False
            for i in cart.listing.all():
                 # 检查是否有人比你提前支付
                try:
                    check_order = ListOrder.objects.get(list_pk=i,status='Paid')
                    # 删除订单
                    list_order = ListOrder.objects.get(list_pk=i,buyer_id=request.user.username)
                    list_order.delete()
                    need_refund = True
                except:
                    # 添加order config文件信息
                    config = configparser.ConfigParser()
                    user_discord = request.user.profile.discordid
                    seller = User.objects.get(username=i.user)
                    seller_discord = seller.profile.discordid
                    start_time = i.start_time
                    end_time = i.end_time
                    start_time = ",".join(start_time.split())
                    end_time = ",".join(end_time.split())
                    # 订单号命名方式：type+pk
                    config['1'+'#'+str(i.pk)] = {
                        'bot': i.bot,
                        'start_time': start_time,
                        'end_time': end_time,
                        'reset_time': 'RightNow',
                        'buyer': user_discord,
                        'seller' : seller_discord,
                        'key' : i.key,
                        'key_nickname' : i.key_nickname,
                        'Reason' : 'None',
                        'order_buyer' : '!order_buyer %(Bot)s %(Start_time)s %(End_time)s %(Buyer)s <@%(Buyer)s>',
                        'order_seller' : '!order_seller %(Bot)s %(Start_time)s %(End_time)s <@%(Seller)s>',
                        'reset_buyer' : '!reset_buyer %(Bot)s %(Key)s <@%(Buyer)s>',
                        'reset_seller' : '!reset_seller %(Bot)s %(Key)s %(Key_nickname)s %(Reset_time)s <@%(Seller)s>',
                        'reset_cancel_seller' : '!reset_cancel_seller %(Bot)s %(Key)s %(Key_nickname)s <@%(Seller)s>',
                        'end_buyer' : '!end_buyer %(Bot)s %(Key)s %(Start_time)s %(End_time)s %(Buyer)s <@%(Buyer)s>',
                        'end_seller' : '!end_seller %(Bot)s %(Key)s %(Key_nickname)s %(Start_time)s %(End_time)s <@%(Seller)s>',
                        'auto_reset' : '!reset_command %(Bot)s %(Key)s %(Key_nickname)s %(Seller)s <@%(Seller)s>',
                        'cancel_buyer' : '!cancel_buyer %(Bot)s %(reason)s <@%(Buyer)s>',
                        'cancel_seller' : '!cancel_seller %(Bot)s %(reason)s <@%(Seller)s>',
                        'start_seller' : '!start_seller %(Bot)s %(Key)s %(Key_nickname)s %(Start_time)s %(End_time)s <@%(Seller)s>',
                        'start_buyer' : '!start_buyer %(Bot)s %(Key)s %(Key_nickname)s %(Start_time)s %(End_time)s <@%(Buyer)s>',
                    }
                    with open('order_config.cfg', 'a') as configfile:
                        config.write(configfile)

                    # order变为paid
                    list_order = ListOrder.objects.get(list_pk=i,buyer_id=request.user.username)
                    # 修改用户钱包数据
                    if flag:
                        wallet = Wallet.objects.get(user=request.user)
                        wallet.points -= list_order.points
                        wallet.total -= list_order.balance
                        wallet.save()
                        flag = False
                    list_order.status = 'Paid'
                    list_order.save()
                    # Listing变为unshow
                    temp = BotListing.objects.get(pk=i.pk)
                    temp.status = 'Unshow'
                    temp.save()
                    # 创建rental表
                    start_time = temp.start_time
                    end_time = temp.end_time
                    result,listing = compare_time(start_time, end_time)
                    if result == False:
                        rental_status = 'Upcoming'
                    else:
                        rental_status = 'Active'
                    
                    rental = Rental.objects.create(seller_id=i.user, buyer_id=request.user.username,rental_status=rental_status,listing_num=i.pk,rental_from='Normal')
                    # 检查卖家的时间重叠，删除相应的listing
                    bot = i.bot
                    key = i.key
                    start_time = i.start_time
                    end_time = i.end_time
                    listing = BotListing.objects.filter(user=i.user,bot=bot,key=key,status='Show')
                    for j in listing:
                        result = compare_time_when_listing(j.start_time,start_time,j.end_time,end_time)
                        if result == False:
                            j.delete()
                    # 给seller count加一
                    seller_obj = User.objects.get(username=i.user)
                    seller = Seller.objects.get(user=seller_obj)
                    seller.sell_count += 1
                    seller.save()
                    
                    # 给每一个卖家发送dc message,买家也发
                    order_number = '1'+'#'+ str(i.pk)
                    command_field(order_number, 'order_seller','order')
                    command_field(order_number, 'order_buyer','order')

                    
            # buyer count加一, 添加points
            buyer = Buyer.objects.get(user=request.user)
            buyer.buy_count += 1
            points = amount*0.01
            buyer.points += points
            buyer.save()

            # 清空购物车数据
            cart.listing.clear()
            if need_refund == True:
                data['status'] = 'Refund'
                # 执行退款
                alipay = aliPay()
                query_params = alipay.api_alipay_trade_refund(
                    out_trade_no=out_trade_no,  # 商户订单号  这里一般是从前端传过来的数据
                    refund_amount=amount,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
                )
            else:
                data['status'] = 'Payment Success!'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'unsuccess':
        # 点击cancel后删除订单
        cart = ItemInCart.objects.get(user=request.user)
        for i in cart.listing.all():
            list_order = ListOrder.objects.get(list_pk=i,buyer_id=request.user.username,status='Unpaid')
            list_order.delete()
    elif request.POST.get('flag') == 'get_bid':
        data = {}
        bid_str = request.POST.get('bid_pk')
        bid_str = bid_str.strip('[]')
        bid_num = bid_str.split(",")

        key_str = request.POST.get('key')
        key_str = key_str.strip('[]')
        key = key_str.split(",")
        for i in key:
            i = i.strip('"')
            bot = BotInventory.objects.get(key=i)

        counter = Counter(key)

        for i,j in zip(key,bid_num):
            # 检查重叠性
            if counter[i]>=2:
                for m,n in zip(key,bid_num):
                    if i == m:
                        bid_j = BotBidding.objects.get(pk=j)
                        bid_n = BotBidding.objects.get(pk=n)
                        result = compare_time_when_listing(bid_j.start_time,bid_n.start_time,bid_j.end_time,bid_n.end_time)
                        if result == False:                   
                            data['status'] = 'Overlap'
                            return JsonResponse(data)

            # 把bidlist中改成unpaid，提醒买家该付款了
            bid = BotBidding.objects.get(pk=j)
            bid.payment_status = 'Unpaid'
            # bid表中不显示，不允许别人bid
            bid.status = 'Unshow'
            # 添加卖家选择的key到bid order表中
            i = i.strip('"')
            bot = BotInventory.objects.get(key=i)
            key = bot.key
            nickname = bot.key_nickname
            # 设置创建时间，计算remove的时间
            order_time = datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            remove_time = (order_time+datetime.timedelta(minutes=1)).replace(tzinfo=pytz.timezone('UTC'))
            # 创建一个bid order表，状态为unpaid，锁车15分钟
            bid.order_time = order_time
            bid.remove_time = remove_time
            bid.key = key
            bid.key_nickname = nickname
            bid.save()
            bid_order = BidOrder.objects.create(bid_pk=bid, seller_id=request.user.username, status='Unpaid',key=key,key_nickname=nickname,order_time=order_time,remove_time=remove_time)
            # 删除卖家购物车中的内容
            cart = ItemInCart.objects.get(user=request.user)
            cart.bidding.clear()
            cart.save()

        data['status'] = 'Success'
        return JsonResponse(data)

    return render(request, 'cart.html', context)


def result(request):
    params = request.GET.dict()
    sign = params.pop('sign', None)
    alipay = aliPay()
    status = alipay.verify(params, sign)
    if status: 
        context = {
            'info': 'success',
        }
        return render(request, 'paid.html', context)
    return HttpResponse('支付失败')