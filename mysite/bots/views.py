from django.shortcuts import render,redirect
from .models import Bot, BotListing, Order, BotBidding
from cart.models import ItemInCart
from user.models import Buyer, Wallet, Seller
from django.contrib.auth.models import User
from .forms import SearchForm
import time
from urllib.parse import parse_qs
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .wx_pay import get_sign, trans_xml_to_dict, trans_dict_to_xml
from django.views.decorators.csrf import csrf_exempt
import requests
from mysite.compare_time import compare_time, compare_time_when_listing

# Create your views here.
def bot_list(request):
    all_bots = Bot.objects.all()
    context = {
        'all_bots': all_bots,
    }
    return render(request, 'bot_list.html', context)

def bot_detail(request, name):
    searchform = SearchForm()
    bot_info = Bot.objects.filter(name=name)
    context = {
        'searchform': searchform,
        'bot_info': bot_info,
        'bot': name,
    }
    return render(request, 'bot_detail.html', context)

@csrf_exempt
def listing(request, bot):
    botlisting = BotListing.objects.filter(bot=bot, status='Show')
    botbidding = BotBidding.objects.filter(bot=bot,status='Show')
    context = {
        'botlisting': botlisting,
        'botbidding': botbidding,
    }
    if request.POST.get('flag') == 'buyercart':
        data = {}
        listing_num = request.POST.get('listing_num')
        user = request.user
        listing = BotListing.objects.get(pk=listing_num)
        cart = ItemInCart.objects.get(user=user)
        for i in cart.listing.all():
            # 检查该listing是否已存在于购物车中
            if i == listing:
                data['status'] = 'Item already in cart'
                return JsonResponse(data)
            # 不允许添加同一个买家的重叠时间的key于购物车中
            seller = i.user
            start_time = i.start_time
            end_time = i.end_time
            bot = i.bot
            key = i.key
            new_start_time = listing.start_time
            new_end_time = listing.end_time
            result = compare_time_when_listing(new_start_time,start_time,new_end_time,end_time)
            if result == False:
                data['status'] = "Can't add the same key that has the overlapping time, please choose another one!"
                return JsonResponse(data)

        cart.listing.add(listing)
        cart.save()
        data['status'] = 'Successfully add to cart'
        return JsonResponse(data)

    elif request.POST.get('flag') == 'sellercart':
        data = {}
        listing_num = request.POST.get('listing_num')
        user = request.user
        listing = BotBidding.objects.get(pk=listing_num)
        cart = ItemInCart.objects.get(user=user)
        for i in cart.bidding.all():
            if i == listing:
                data['status'] = 'Item already in cart'
                return JsonResponse(data)
        cart.bidding.add(listing)
        cart.save()
        data['status'] = 'Successfully add to cart'
        return JsonResponse(data)
    
    return render(request, 'listing.html', context)

@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    if request.method == 'POST':
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        alipay = aliPay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 1.修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            
            # 2. 根据订单号将数据库中的数据进行更新
            listing = BotListing.objects.get(listing=out_trade_no)
            order = Order.objects.get(listing=listing)
            order.status = 'Paid'
            order.save()
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')
    return HttpResponse('')


@csrf_exempt
def pay_result(request):
    """
    支付完成后，跳转回的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)

    alipay = aliPay()

    status = alipay.verify(params, sign)

    if status:
        return HttpResponse(status)
    return HttpResponse('支付失败')