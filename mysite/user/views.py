from django.shortcuts import render, get_object_or_404,redirect
from read_statistics.utils import get_week_read_date
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from django.contrib import auth
import datetime
from django.urls import reverse
from .forms import LoginForm, RegForm, TimezoneForm, RequestVerifyForm, ChangeNicknameForm, GeneralListingForm, CustomListingForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
import requests
from .models import Profile, BotInventory, Verify, Seller, Buyer, Wallet, Rental, Transaction
from bots.models import BotListing, Bot, BotBidding, BidOrder
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .test import test
from pythonProject.command_field import command_field
from django.db import IntegrityError
import json
import os
import sys
import configparser
from django.conf import settings
from django.core import serializers
from mysite.compare_time import compare_time, compare_time_when_listing, list_time
from cart.alipay import AliPay
import datetime
import pytz
from cart.models import ItemInCart
from django.contrib.auth.hashers import check_password
# from scheduler.views import scheduler




# Create your views here.
@csrf_exempt
def login(request):
    # POST步骤：获取用户提交的表单的信息
    if request.POST.get('flag') == 'login':
        password = request.POST.get('password')
        username = request.POST.get('username')
        data = {}
        try:
            user = User.objects.get(username=username)
        except:
            data['status'] = 'user'
            return JsonResponse(data)
        pwd = user.password
        if check_password(password, pwd):
            auth.login(request, user)
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            data['status'] = 'password'
            return JsonResponse(data)

        # login_form = LoginForm(request.POST)
        # if login_form.is_valid():
        #     user = login_form.cleaned_data['user']
            # auth.login(request, user)
        #     return redirect(request.GET.get('from', reverse('home')))

    # GET步骤：就是获取页面，表单为空
    else:
        context = {}
        return render(request, 'login.html', context)
@csrf_exempt
def register(request):
    # POST步骤：获取用户提交的表单的信息
    if request.POST.get('flag') == 'register':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        user = User.objects.create_user(username, email, password)   # 在数据库中注册user
        user.save()
        buyer = Buyer.objects.create(user=user)
        seller = Seller.objects.create(user=user)
        wallet = Wallet.objects.create(user=user)
        cart = ItemInCart.objects.create(user=user)
        buyer.save()
        seller.save()
        wallet.save()
        cart.save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        data = {}
        data['status'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'get_info':
        user_all = User.objects.all()
        username = []
        email = []
        for i in user_all:
            username.append(i.username)
            email.append(i.email)

        context = {
        'username': username,
        'email': email,
        }
        return JsonResponse(context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def aliPay():
    obj = AliPay(
        appid="2021000118614830",                              # 支付宝沙箱里面的APPID，需要改成你自己的
        app_notify_url='http://localhost:8000/cart/check_order/',  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        return_url="http://localhost:8000/user/result/",            # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
        alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
        app_private_key_path=settings.APP_PRIVATE,      # 应用私钥
        debug=True,  # 默认False,True表示使用沙箱环境测试
    )
    return obj

def user_info(request):
    if request.method == 'POST':
        verify_form = RequestVerifyForm(request.POST)
        data = {}
        # change nickname
        if request.POST.get('flag') == 'nickname':
            nickname = request.POST.get('nickname')
            bot = request.POST.get('bot')
            key = request.POST.get('key')
            temp= BotInventory.objects.get(user_id=request.user.username, user_discord=request.user.profile.discordid, bot=bot, key=key)
            temp.key_nickname = nickname
            temp.save()
            data['status'] = 'SUCCESS_NICKNAME'
        elif request.POST.get('flag') == 'savechanges':
            timezone = request.POST.get('timezone')
            email = request.POST.get('email')
            user = User.objects.get(username=request.user.username)
            user.email = email
            user.save()
            profile = Profile.objects.get(user=request.user)
            profile.timezone = timezone
            profile.save()
            data = {}
            data['status'] = 'success'
            return JsonResponse(data)

        elif request.POST.get('flag') == 'confirm_reset':
            bot = request.POST.get('bot')
            key = request.POST.get('key')
            temp= BotInventory.objects.get(user_id=request.user.username, user_discord=request.user.profile.discordid, bot=bot, key=key)
            temp2 = Verify.objects.get(user_id=request.user.username, user_discord=request.user.profile.discordid, bot=bot, key=key)
            temp.need_reset = False
            temp2.need_reset = False
            temp.save()
            temp2.save()
            # 发送discord信息
            data['status'] = 'SUCCESS_CONFIRM_RESET'
        elif request.POST.get('flag') == 'twitter':
            link = request.POST.get('link')
            seller = Seller.objects.get(user=request.user)
            seller.twitter_link = link
            seller.save()
            data['status'] = 'SUCCESS_ADD_LINK'
        elif request.POST.get('flag') == 'topup':
            try:
                amount = float(request.POST.get('amount'))
            except:
                pay_url = ''
                return JsonResponse(pay_url, safe=False)

            # 实例化SDK里面的类AliPay
            alipay = aliPay()

            topup = Transaction.objects.create(user=request.user.username,amount=amount,status='Processing',use='topup')
            now = datetime.datetime.now()
            now_str = now.strftime('%Y%m%d')
            out_trade_no = now_str + '3' + str(topup.pk)
            topup.alipay_no = out_trade_no
            topup.save()
            query_params = alipay.direct_pay(
                subject="Topup#" + str(topup.pk),  # 商品简单描述 这里一般是从前端传过来的数据
                out_trade_no=out_trade_no,  # 商户订单号  这里一般是从前端传过来的数据
                total_amount=amount,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
            )
            # 拼接url，转到支付宝支付页面
            pay_url = "https://openapi.alipaydev.com/gateway.do?"+query_params
            return JsonResponse(pay_url, safe=False)
        elif request.POST.get('flag') == 'check_success':
            alipay = aliPay()
            #获取订单号
            topup = Transaction.objects.get(user=request.user.username,status='Processing',use='topup')
            out_trade_no = topup.alipay_no

            # 查询交易状态
            response = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
            data = {}
            if response['alipay_trade_query_response']['code'] == '40004':
                data['status'] = 'Payment is still processing!'
            if response['alipay_trade_query_response']['code'] == '10000':
                topup = Transaction.objects.get(alipay_no=out_trade_no)
                amount = topup.amount
                user_id = topup.user
                user = User.objects.get(username=user_id)

                # 修改用户钱包数据
                if topup.status != 'Paid':
                    wallet = Wallet.objects.get(user=user)
                    wallet.withdraw_able += amount
                    wallet.total = wallet.withdraw_able + wallet.freeze
                    wallet.save()
                    # 把cart响应内容变成paid
                    topup.status = 'Paid'
                    topup.save()
                data['status'] = 'Payment Success!'
            return JsonResponse(data)
        elif request.POST.get('flag') == 'unsuccess':
            # 点击cancel后删除订单
            topup = Transaction.objects.get(user=request.user.username,status='Processing',use='topup')
            topup.delete()
        elif request.POST.get('flag') == 'withdrawal':
            data = {}
            try:
                amount = float(request.POST.get('amount'))
            except:
                data['status'] = 'fail'
                return JsonResponse(data)
            wallet = Wallet.objects.get(user=request.user)
            alipay_id = wallet.alipay_id
            trans = Transaction.objects.create(user=request.user.username,amount=amount,use='withdrawal',status='Processing',alipay_id=alipay_id)   
            wallet.withdraw_able -= amount
            wallet.total = wallet.withdraw_able + wallet.freeze
            wallet.save()
            # 添加payout config文件信息
            config = configparser.ConfigParser()
            user_discord = request.user.profile.discordid
            pk = trans.pk
            config[user_discord+'#'+str(pk)] = {
                'Seller' : user_discord,
                'Amount' : amount,
                'Method' : 'Alipay',
                'Reason' : 'Account not found',
                'payout_denied' : '!payout_denied %(Amount)s %(Method)s %(Reason)s <@%(Seller)s>',
                'payout_request' : '!payout_request %(Amount)s %(Method)s <@%(Seller)s>',
                'payout_succeed' : '!payout_succeed %(Amount)s %(Method)s <@%(Seller)s>',
            }
            with open('payout_config.cfg', 'a') as configfile:
                config.write(configfile)
            # 发送dc message
            order_number = user_discord+'#'+ str(pk)
            command_field(order_number, 'payout_request','payout')
            data['status'] = 'success'
            return JsonResponse(data)


        elif request.POST.get('flag') == 'change_alipay_account':
            account = request.POST.get('account')
            wallet = Wallet.objects.get(user=request.user)
            wallet.alipay_id = account
            wallet.save()
    else:      
        user = request.user
        verify_form = RequestVerifyForm()
        buyer_info = Buyer.objects.get(user=user)
        seller_info = Seller.objects.get(user=user)
        wallet = Wallet.objects.get(user=user)
        userinfo = User.objects.get(username=user)
        # 检查并删除未完成的订单
        topup = Transaction.objects.filter(user=request.user.username,status='Processing',use='topup')
        for i in topup:
            i.delete()

        context = {
            'verify_form' : verify_form,
            'seller_info' : seller_info,
            'buyer_info' : buyer_info,
            'wallet' : wallet,
            'user': userinfo,
        }
        return render(request, 'user_info.html', context)

def result(request):
    params = request.GET.dict()
    sign = params.pop('sign', None)
    alipay = aliPay()
    status = alipay.verify(params, sign)
    if status: 
        context = {
            'info': 'success',
        }
        return render(request, 'topup.html', context)
    return HttpResponse('支付失败')


DISCORD_URL = 'https://discord.com/api/oauth2/authorize?client_id=883718490761084938&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fuser%2Flogin%2Foauth2%2Fredirect&response_type=code&scope=identify%20guilds.join%20guilds%20connections'
CLIENT_ID = '883718490761084938'
CLIENT_SECRET = 'HmhaYoLFF-k3GA3R6qjdWD3CNuQIB-r3'
REDIRECT_URI = 'http://localhost:8000/user/login/oauth2/redirect'
API_ENDPOINT = "https://discord.com/api"
GUILDID = '850597103783641128'
BOTTOKEN = 'ODgzNzE4NDkwNzYxMDg0OTM4.YTOA-g.tG4oy_fyMINjsBYXEVA8kGZF1cA'
API_ENDPOINT_JOIN = "https://discord.com/api/v8"

def add_to_guild(access_token, guildID, userID, bottoken):
    url = f"{API_ENDPOINT_JOIN}/guilds/{guildID}/members/{userID}"
    data = {
        "access_token" : access_token,
    }
    headers = {
        "Authorization" : "Bot %s" %  bottoken,
        'Content-Type': 'application/json'
    }
    response = requests.put(url=url, headers=headers, json=data)
    print(response.text)

def exchange_code(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    credentidals = r.json()
    access_token = credentidals['access_token']
    response = requests.get('%s/v8/users/@me' % API_ENDPOINT, headers={ 'Authorization' : 'Bearer %s' % access_token})
    user = response.json()
    return user, access_token

def discord_login(request):
    discord_url = DISCORD_URL
    return redirect(discord_url)

def discord_login_redirect(request):
    code = request.GET.get('code')
    discord_info, access_token = exchange_code(code)
    user = request.user
    avatar_url = 'https://cdn.discordapp.com/avatars/' + discord_info['id'] + '/' + discord_info['avatar'] + '.png'
    profile, created = Profile.objects.get_or_create(user = request.user)
    profile.discordavatar = avatar_url
    profile.discordname = discord_info['username']
    profile.discordid = discord_info['id']
    
    # 一个discord只能绑定一个账号
    if Profile.objects.filter(discordid=discord_info['id']).exists():
        messages.error(request, '该Discord账户已被绑定，请更换重试。')
        return redirect('user_info')
    elif not Profile.objects.filter(discordid=discord_info['id']).exists():         
        profile.connected = True
        add_to_guild(access_token, GUILDID, discord_info['id'] , BOTTOKEN)
        profile.save()
        # messages.warning(request, '绑定成功。')
        return redirect('user_info')

def disconnect_discord(request):
    profile, created = Profile.objects.get_or_create(user = request.user)
    profile.discordname = ''
    profile.discordid = ''
    profile.connected = False
    profile.save()
    messages.success(request, '解绑成功。')
    return redirect('user_info')

def select_timezone(request):
    if request.method == 'POST':
        timezone_form = TimezoneForm(request.POST)
        if timezone_form.is_valid():
            profile, created = Profile.objects.get_or_create(user = request.user)
            timezone_value = request.POST.get('timezone', "")
            profile.timezone = timezone_value
            profile.save()
            return redirect('user_info')
    else:      
        timezone_form = TimezoneForm()
        context = {
            'timezone_form' : timezone_form,
        }
        print(timezone_form)
        return render(request, 'timezone.html', context)

@csrf_exempt
def admin_verify(request):
    data = {}
    if request.method == 'POST':
        # 请求用户reset以检查key
        if request.POST.get('flag') == 'request_reset':
            username = request.POST.get('user')
            ID = request.POST.get('ID')
            bot = request.POST.get('bot')
            key = request.POST.get('key')
            temp= BotInventory.objects.get(user_id=username, user_discord=ID, bot=bot, key=key)
            temp2 = Verify.objects.get(user_id=username, user_discord=ID, bot=bot, key=key)
            temp.need_reset = True
            temp2.need_reset = True
            temp.save()
            temp2.save()
            # 发送discord信息
            order_number = ID+'#'+key
            command_field(order_number, 'keycheck_reset','key')
            data['status'] = 'SUCCESS_REQUEST_RESET'
        # 取消请求
        elif request.POST.get('flag') == 'cancel_reset':
            username = request.POST.get('user')
            ID = request.POST.get('ID')
            bot = request.POST.get('bot')
            key = request.POST.get('key')
            temp= BotInventory.objects.get(user_id=username, user_discord=ID, bot=bot, key=key)
            temp2 = Verify.objects.get(user_id=username, user_discord=ID, bot=bot, key=key)
            temp.need_reset = False
            temp2.need_reset = False
            temp.save()
            temp2.save()
            data['status'] = 'SUCCESS_CANCEL_RESET'

        else:
            status = request.POST.get('status')
            user = request.POST.get('user')
            ID = request.POST.get('ID')
            bot = request.POST.get('bot')
            key = request.POST.get('key')

            temp, created = Verify.objects.get_or_create(user_id=user, user_discord=ID, bot=bot, key=key)
            temp_inventory, created = BotInventory.objects.get_or_create(user_id=user, user_discord=ID, bot=bot, key=key)
            if status == 'pass':   
                temp.status = 'Ready to be listed'
                temp_inventory.status = 'Ready to be listed'
                # 发送discord信息
                order_number = ID+'#'+key
                command_field(order_number, 'keycheck_success','key')
            if status == 'fail':
                temp.status = 'Not Verified'
                temp_inventory.status = 'Not Verified'
                # 发送discord信息
                order_number = ID+'#'+key
                command_field(order_number, 'keycheck_fail','key')
                
            temp_inventory.save()
            temp.save()
            data['status'] = 'SUCCESS'

        return JsonResponse(data)
    
    all_data = Verify.objects.all()
    context = {
        'all_data' : all_data
    }
    return render(request, 'verify.html', context)

def my_purchase(request):
    user = request.user
    generallistingform = GeneralListingForm()
    customlistingform = CustomListingForm()

    if request.POST.get('flag') == 'delete_bidding':
        num_bidding = request.POST.get('num_bidding')
        temp = BotBidding.objects.get(pk=num_bidding)
        price = float(request.POST.get('price'))
        wallet = Wallet.objects.get(user=user)
        wallet.withdraw_able += price
        wallet.save()
        temp.delete()
        data = {}
        data['status'] = 'SUCCESS_DELETE_BIDDING'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'resetlater':
        num_listing = request.POST.get('num_listing')
        way =  request.POST.get('type')
        time = request.POST.get('time')
        user = request.user.username
        if way == 'Normal':
            order = Rental.objects.get(buyer_id=user,listing_num=num_listing,rental_from=way)
            listing = BotListing.objects.get(pk=num_listing,status='Unshow')
            listing.keyreset_status = 'Waiting for reset'
            listing.keyreset_time = time
            listing.request_time = datetime.datetime.now()
            listing.save()
            # 添加reset time
            time = ",".join(time.split())
            config.set(order_number, 'reset_time', time)
            with open('order_config.cfg', 'wb') as config_file:
                config.write(config_file)
            # 给seller发reset信息
            order_number = '1'+'#'+ str(listing.pk)
            command_field(order_number, 'reset_seller','order')
        else:
            order = Rental.objects.get(buyer_id=user,bidding_num=num_listing,rental_from=way)
            listing = BotBidding.objects.get(pk=num_listing,status='Unshow')
            listing.keyreset_status = 'Waiting for reset'
            listing.keyreset_time = time
            listing.request_time = datetime.datetime.now()
            listing.save()
            # 添加reset time
            time = ",".join(time.split())
            config.set(order_number, 'reset_time', time)
            with open('order_config.cfg', 'wb') as config_file:
                config.write(config_file)
            # 给seller发reset信息
            order_number = '2'+'#'+ str(listing.pk)
            command_field(order_number, 'reset_seller','order')
        order.keyreset_status = 'Waiting for reset'
        order.keyreset_time = time
        order.request_time = datetime.datetime.now()
        order.save()
        data = {}
        data['status'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'resetnow':
        num_listing = request.POST.get('num_listing')
        way =  request.POST.get('type')
        user = request.user.username
        if way == 'Normal':
            order = Rental.objects.get(buyer_id=user,listing_num=num_listing,rental_from=way)
            listing = BotListing.objects.get(pk=num_listing,status='Unshow')
            listing.keyreset_status = 'Waiting for reset'
            listing.request_time = datetime.datetime.now()
            listing.save()
            # 给seller发reset信息
            order_number = '1'+'#'+ str(listing.pk)
            command_field(order_number, 'reset_seller','order')
        else:
            order = Rental.objects.get(buyer_id=user,bidding_num=num_listing,rental_from=way)
            listing = BotBidding.objects.get(pk=num_listing,status='Unshow')
            listing.keyreset_status = 'Waiting for reset'
            listing.request_time = datetime.datetime.now()
            listing.save()
            # 给seller发reset信息
            order_number = '2'+'#'+ str(listing.pk)
            command_field(order_number, 'reset_seller','order')
        order.keyreset_status = 'Waiting for reset'
        order.request_time = datetime.datetime.now()
        order.save()
        data = {}
        data['status'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'submit_editing':
        num_listing = request.POST.get('num_listing')
        print(num_listing)
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        listing_type = request.POST.get('listing_type').strip()
        if listing_type == 'General Rental':
            # 把时间格式改为包括时分秒的格式
            addon = ' 08:00'
            start_time = start_time + addon
            end_time = end_time + addon
        # start_time = request.POST.get('start_time')
        # end_time = request.POST.get('end_time')
        price = float(request.POST.get('price'))
        # print(price)
        temp = BotBidding.objects.get(pk=num_listing)
        data = {}
        temp.start_time = start_time
        temp.end_time = end_time
        temp.listing_type = listing_type
        temp.price = price
        temp.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)

    else:
        bots = Bot.objects.all()
        active_rental = Rental.objects.filter(buyer_id=user.username, rental_status='Active')
        upcoming_rental = Rental.objects.filter(buyer_id=user.username, rental_status='Upcoming')
        past_rental = Rental.objects.filter(buyer_id=user.username, rental_status='Past')
        bidding = BotBidding.objects.filter(user=user.username)
        active_rental_array = []
        upcoming_rental_array = []
        past_rental_array = []
        for i in active_rental:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                active_rental_array.append([BotBidding.objects.get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal':
                active_rental_array.append([BotListing.objects.get(pk=i.listing_num),'Normal'])
        for i in upcoming_rental:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                upcoming_rental_array.append([BotBidding.objects.values('pk','bot','start_time','end_time','price').get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal': 
                upcoming_rental_array.append([BotListing.objects.values('pk','bot','start_time','end_time','price').get(pk=i.listing_num),'Normal'])
        for i in past_rental:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                past_rental_array.append([BotBidding.objects.values('pk','bot','start_time','end_time','price').get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal': 
                past_rental_array.append([BotListing.objects.values('pk','bot','start_time','end_time','price').get(pk=i.listing_num),'Normal'])
        context = {
            'active_rental': active_rental_array,
            'upcoming_rental': upcoming_rental_array,
            'past_rental': past_rental_array,
            'bots': bots,
            'bidding': bidding,
        }
        return render(request, 'my_purchase.html', context)

def trans(request):
    if request.POST.get('flag') == 'confirm':
        pk = request.POST.get('pk')
        trans = Transaction.objects.get(pk=pk)
        trans.status = 'Paid'
        trans.save()
        # 发送dc message
        user = trans.user
        user_obj = User.objects.get(username=user)
        dc_id = user_obj.profile.discordid
        order_number = dc_id+'#'+ str(pk)
        command_field(order_number, 'payout_succeed','payout')
    if request.POST.get('flag') == 'deny':
        pk = request.POST.get('pk')
        trans = Transaction.objects.get(pk=pk)
        trans.status = 'Failed'
        trans.save()
        # 发送dc message
        user = trans.user
        user_obj = User.objects.get(username=user)
        dc_id = user_obj.profile.discordid
        order_number = dc_id+'#'+ str(pk)
        command_field(order_number, 'payout_denied','payout')

    all_data = Transaction.objects.all()
    context = {
        'all_data' : all_data
    }
    return render(request, 'trans.html', context)

def mybot(request):
    # key verify
    if request.POST.get('flag') == 'addbot':
        data = {}
        bot = request.POST.get('bot')
        if bot =='请选择一个bot' or bot == '':
            data['status'] = 'nobot'
            return JsonResponse(data)
        key = request.POST.get('key')
        if key =='':
            data['status'] = 'nokey'
            return JsonResponse(data)
        nickname = request.POST.get('nickname')
        verify_info = Verify.objects.create(user_id=request.user.username, user_discord=request.user.profile.discordid, bot=bot, key=key)
        bot_obj = Bot.objects.get(name=bot)
        bot_inventory = BotInventory.objects.create(user_id=request.user.username, user_discord=request.user.profile.discordid, bot=bot, key=key, key_nickname=nickname,img_url=bot_obj.img_url, status='Processing Verification')
        bot_inventory.save()
        verify_info.save()
        # 添加keycheck config文件信息
        config = configparser.ConfigParser()
        user_discord = request.user.profile.discordid
        config[user_discord+'#'+key] = {
            'Bot': bot,
            'Seller' : user_discord,
            'Key' : key,
            'Key_nickname' : nickname,
            'Reason' : 'None',
            'keycheck_fail' : '!keycheck_fail %(Bot)s %(Key)s %(Key_nickname)s %(Reason)s <@%(Seller)s>',
            'keycheck_success' : '!keycheck_success %(Bot)s %(Key)s %(Key_nickname)s <@%(Seller)s>',
            'keycheck_reset' : '!keycheck_reset %(Bot)s %(Key)s %(Key_nickname)s <@%(Seller)s>',
        }
        with open('keycheck_config.cfg', 'a') as configfile:
            config.write(configfile)
        data['status'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'delete_listing':
        data = {}
        pk = request.POST.get('num_listing')
        listing = BotInventory.objects.get(pk=pk)
        if listing.status == 'Listed':
            data['status'] = 'listing'
            return JsonResponse(data)
        else:
            listing.delete()
            data['status'] = 'success'
            return JsonResponse(data)
    elif request.POST.get('flag') == 'step1':
        user = request.user
        userbot = request.POST.get('userbot')
        keys = BotInventory.objects.filter(user_id=user.username, bot=userbot, status='Ready to be listed')
        keys = serializers.serialize("json", keys)
        return HttpResponse(keys)
    elif request.POST.get('flag') == 'submit_listing':
        data = {}
        user = request.user
        bot = request.POST.get('bot')
        if bot == '请选择一个bot' or bot == '':
            data['status'] = 'bot'
            return JsonResponse(data)
        key = request.POST.get('key').strip()
        key = key.split(')')[1]
        if key == '请选择一个key' or key == '':
            data['status'] = 'key'
            return JsonResponse(data)
        find_nickname = BotInventory.objects.get(user_id=user.username,bot=bot,key=key)
        key_nickname = find_nickname.key_nickname
        find_boturl = Bot.objects.get(name=bot)
        boturl = find_boturl.img_url
        listing_type = request.POST.get('listing_type').strip()
        if listing_type == '普通租赁':
            listing_type = 'General Rental'
        else:
            listing_type = 'Custom Rental'
        start_time = request.POST.get('start_time')
        if start_time == '':
            data['status'] = 'time'
            return JsonResponse(data)
        end_time = request.POST.get('end_time')
        if end_time == '':
            data['status'] = 'time'
            return JsonResponse(data)
        if listing_type == 'General Rental':
            # 把时间格式改为包括时分秒的格式
            addon = ' 08:00'
            start_time = start_time + addon
            end_time = end_time + addon
        # 结束时间应大于开始时间
        result = list_time(start_time,end_time)
        if result == False:
            data['status'] = 'time'
            return JsonResponse(data)
        try:
            rmb_price = float(request.POST.get('rmb_price'))
        except:
            data['status'] = 'price'
            return JsonResponse(data)
        try:
            usd_price = float(request.POST.get('usd_price'))
        except:
            data['status'] = 'price'
            return JsonResponse(data)
        user_timezone = user.profile.timezone
        user_level = user.seller.level
        user_sellingnum = user.seller.sell_count
        user_refs = user.seller.Refs
        
        data = {}
        data['status'] = 'SUCCESS'
        # 检查key的重叠性：1检查所有unshow的listing，新的listing不能跟任何一个unshow的listing重叠
        check_time = BotListing.objects.filter(user=user.username,bot=bot,key=key,status='Unshow')
        for i in check_time:
            result = compare_time_when_listing(i.start_time,start_time,i.end_time,end_time)
            if result == False:
                data['status'] = 'FAIL'
                return JsonResponse(data)
        # 检查key的重叠性：2检查所有paid的bidding，新的listing不能跟任何一个paid的bidding重叠
        check_time = BidOrder.objects.filter(seller_id=user.username,key=key,status='Paid')
        for i in check_time:
            result = compare_time_when_listing(i.bid_pk.start_time,start_time,i.bid_pk.end_time,end_time)
            if result == False:
                data['status'] = 'FAIL'
                return JsonResponse(data)
        temp = BotListing.objects.create(user=user.username, bot=bot,img_url=boturl,key=key,key_nickname=key_nickname, \
                                listing_type=listing_type,start_time=start_time,end_time=end_time,rmb_price=rmb_price, \
                                usd_price=usd_price,user_timezone=user_timezone,user_level=user_level,user_sellingnum=user_sellingnum,user_refs=user_refs)
        temp.save()
        bot = BotInventory.objects.get(user_id=user.username,bot=bot,key=key)
        bot.status = 'Listed'
        bot.save()
        return JsonResponse(data)
    elif request.POST.get('flag') == 'delete_my_listing':
        num_listing = request.POST.get('num_listing')
        temp = BotListing.objects.get(pk=num_listing)
        temp.delete()
        data = {}
        data['status'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'submit_editing':
        user = request.user
        num_listing = float(request.POST.get('num_listing'))
        start_time = request.POST.get('start_time')

        end_time = request.POST.get('end_time')
        listing_type = request.POST.get('listing_type').strip()
        if listing_type == '普通租赁':
            listing_type = 'General Rental'
        else:
            listing_type = 'Custom Rental'
        if listing_type == 'General Rental':
            # 把时间格式改为包括时分秒的格式
            addon = ' 08:00'
            start_time = start_time + addon
            end_time = end_time + addon
        rmb_price = float(request.POST.get('rmb_price'))
        usd_price = float(request.POST.get('usd_price'))
        temp = BotListing.objects.get(pk=num_listing)
        data = {}
        bot = temp.bot
        key = temp.key
        user = request.user
        # 检查key的重叠性：1检查所有unshow的listing，新的listing不能跟任何一个unshow的listing重叠
        check_time = BotListing.objects.filter(user=user.username,bot=bot,key=key,status='Unshow')
        for i in check_time:
            result = compare_time_when_listing(i.start_time,start_time,i.end_time,end_time)
            if result == False:
                data['status'] = 'FAIL'
                return JsonResponse(data)
        # 检查key的重叠性：2检查所有paid的bidding，新的listing不能跟任何一个paid的bidding重叠
        check_time = BidOrder.objects.filter(seller_id=user.username,key=key,status='Paid')
        for i in check_time:
            result = compare_time_when_listing(i.bid_pk.start_time,start_time,i.bid_pk.end_time,end_time)
            if result == False:
                data['status'] = 'FAIL'
                return JsonResponse(data)
        temp.start_time = start_time
        temp.end_time = end_time
        temp.listing_type = listing_type
        temp.rmb_price = rmb_price
        temp.usd_price = usd_price
        temp.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'submit_bidding':
        user = request.user
        data = {}
        bot = request.POST.get('bot')
        if bot == '请选择一个bot' or bot == '':
            data['status'] = 'bot'
            return JsonResponse(data)
        listing_type = request.POST.get('listing_type').strip()
        if listing_type == '普通租赁':
            listing_type = 'General Rental'
        else:
            listing_type = 'Custom Rental'
        start_time = request.POST.get('start_time')
        if start_time == '':
            data['status'] = 'time'
            return JsonResponse(data)
        end_time = request.POST.get('end_time')
        if end_time == '':
            data['status'] = 'time'
            return JsonResponse(data)
        if listing_type == 'General Rental':
            # 把时间格式改为包括时分秒的格式
            addon = ' 08:00'
            start_time = start_time + addon
            end_time = end_time + addon

        result = list_time(start_time,end_time)
        if result == False:
            data['status'] = 'time'
            return JsonResponse(data)
        try:
            rmb_price = float(request.POST.get('rmb_price'))
        except:
            data['status'] = 'price'
            return JsonResponse(data)
        try:
            usd_price = float(request.POST.get('usd_price'))
        except:
            data['status'] = 'price'
            return JsonResponse(data)
        find_boturl = Bot.objects.get(name=bot)
        boturl = find_boturl.img_url
        bid = BotBidding.objects.create(user=user.username,bot=bot,img_url=boturl,listing_type=listing_type,start_time=start_time,end_time=end_time,rmb_price=rmb_price,usd_price=usd_price)
        bid.save()
        data['status'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'delete_my_bidding':
        num_listing = request.POST.get('num_listing')
        temp = BotBidding.objects.get(pk=num_listing)
        temp.delete()
        data = {}
        data['status'] = 'success'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'submit_bid_editing':
        user = request.user
        num_listing = float(request.POST.get('num_listing'))
        start_time = request.POST.get('start_time')

        end_time = request.POST.get('end_time')
        listing_type = request.POST.get('listing_type').strip()
        if listing_type == '普通租赁':
            listing_type = 'General Rental'
        else:
            listing_type = 'Custom Rental'
        if listing_type == 'General Rental':
            # 把时间格式改为包括时分秒的格式
            addon = ' 08:00'
            start_time = start_time + addon
            end_time = end_time + addon
        rmb_price = float(request.POST.get('rmb_price'))
        usd_price = float(request.POST.get('usd_price'))
        temp = BotBidding.objects.get(pk=num_listing)
        data = {}
        temp.start_time = start_time
        temp.end_time = end_time
        temp.listing_type = listing_type
        temp.rmb_price = rmb_price
        temp.usd_price = usd_price
        temp.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'pay':
        num_bidding = request.POST.get('num_bidding')
        row_price = request.POST.get('price')
        price = row_price.split('(')[0]
        price = price.replace('￥', '')
        price = float(price)
        
        alipay = aliPay()
        now = datetime.datetime.now()
        now_str = now.strftime('%Y%m%d')
        out_trade_no = now_str + '1' + str(num_bidding)
        # 给bid order添加订单号,并把状态改为支付中
        bid = BotBidding.objects.get(pk=num_bidding)
        bid_order = BidOrder.objects.get(bid_pk=bid)
        bid_order.status = 'Processing'
        bid_order.alipay_no = out_trade_no
        bid_order.save()
        query_params = alipay.direct_pay(
            subject="Bidpay#" + str(num_bidding),  # 商品简单描述 这里一般是从前端传过来的数据
            out_trade_no=out_trade_no,  # 商户订单号  这里一般是从前端传过来的数据
            total_amount=price,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
        )
        # 拼接url，转到支付宝支付页面
        pay_url = "https://openapi.alipaydev.com/gateway.do?"+query_params
        return JsonResponse(pay_url, safe=False)
    elif request.POST.get('flag') == 'check_success':
        alipay = aliPay()
        #获取订单号
        num_bidding = request.POST.get('num_bidding')
        bid = BotBidding.objects.get(pk=num_bidding)
        bid_order = BidOrder.objects.get(bid_pk=bid,status='Processing')
        out_trade_no = bid_order.alipay_no

        # 查询交易状态
        response = alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        data = {}
        if response['alipay_trade_query_response']['code'] == '40004':
            data['status'] = 'Payment is still processing!'
        if response['alipay_trade_query_response']['code'] == '10000':
            # 添加order config
            config = configparser.ConfigParser()
            user_discord = request.user.profile.discordid
            seller = User.objects.get(username=bid_order.seller_id)
            seller_discord = seller.profile.discordid
            start_time = bid.start_time
            end_time = bid.end_time
            start_time = ",".join(start_time.split())
            end_time = ",".join(end_time.split())
            # 订单号命名方式：type+pk
            config['2'+'#'+str(bid.pk)] = {
                'bot': bid.bot,
                'start_time': start_time,
                'end_time': end_time,
                'reset_time': bid.keyreset_time,
                'buyer': user_discord,
                'seller' : seller_discord,
                'key' : bid.key,
                'key_nickname' : bid.key_nickname,
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

            # bidding表变为paid
            amount = bid.rmb_price
            bid.payment_status = 'Paid'
            bid.save()
            # bid order表变为paid
            order = BidOrder.objects.get(bid_pk=bid)
            order.status = 'Paid'
            order.save()
            # 创建rental表
            start_time = bid.start_time
            end_time = bid.end_time
            result,listing = compare_time(start_time, end_time)
            if result == False:
                rental_status = 'Upcoming'
            else:
                rental_status = 'Active'
            # 检查seller的listing，删除时间重叠的listing
            seller_id = bid_order.seller_id
            start_time = bid.start_time
            end_time = bid.end_time
            listing = BotListing.objects.filter(user=seller_id)
            for i in listing:
                result = compare_time_when_listing(i.start_time,start_time,i.end_time,end_time)
                if result == 'False':
                    i.delete()
            # 给seller count加一
            seller_obj = User.objects.get(username=seller_id)
            seller = Seller.objects.get(user=seller_obj)
            seller.sell_count += 1
            seller.save()
            # buyer count加一, 添加points
            buyer = Buyer.objects.get(user=request.user)
            buyer.buy_count += 1
            points = amount*0.01
            buyer.points += points
            buyer.save()

            rental = Rental.objects.create(seller_id=bid.user,buyer_id=request.user.username,bidding_num=bid.pk,rental_status=rental_status,rental_from='Bid')
            # 发送dc信息
            order_number = '2'+'#'+ str(bid.pk)
            command_field(order_number, 'order_seller','order')
            command_field(order_number, 'order_buyer','order')

            data['status'] = 'Payment Success!'
        return JsonResponse(data)
    elif request.POST.get('flag') == 'unsuccess':
        # 点击cancel后改变status，清除订单号
        num_bidding = request.POST.get('num_bidding')
        bid = BotBidding.objects.get(pk=num_bidding)
        bid_order = BidOrder.objects.get(bid_pk=bid,status='Processing')
        bid_order.status = 'Unpaid'
        bid_order.alipay_no = ''
        bid_order.save()
        data = {}
        return JsonResponse(data)
    elif request.POST.get('flag') == 'submit_reset':
        num_listing = request.POST.get('num_listing')
        way =  request.POST.get('buy_type')
        user = request.user.username
        if way == 'Normal':
            order = Rental.objects.get(seller_id=user,listing_num=num_listing,rental_from=way)
            listing = BotListing.objects.get(pk=num_listing,status='Unshow')
            listing.keyreset_status = 'Nothing'
            listing.request_time = ''
            listing.save()
            # 给buyer发reset信息
            order_number = '1'+'#'+ str(listing.pk)
            command_field(order_number, 'reset_buyer','order')
        else:
            order = Rental.objects.get(buyer_id=user,bidding_num=num_listing,rental_from=way)
            listing = BotBidding.objects.get(pk=num_listing,status='Unshow')
            listing.keyreset_status = 'Nothing'
            listing.request_time = ''
            listing.save()
            # 给buyer发reset信息
            order_number = '2'+'#'+ str(listing.pk)
            command_field(order_number, 'reset_buyer','order')
        order.keyreset_status = 'Nothing'
        order.request_time = ''
        order.save()
        data = {}
        data['status'] = 'success'
        return JsonResponse(data)
    else:
        user = request.user
        bot_list = []
        bot_list = BotInventory.objects.filter(user_id=user.username)
        botlisting = BotListing.objects.filter(user=request.user.username)
        havebot = BotInventory.objects.filter(user_id=user.username).values("bot","img_url").distinct()
        active_rental = Rental.objects.filter(seller_id=user.username, rental_status='Active')
        upcoming_rental = Rental.objects.filter(seller_id=user.username, rental_status='Upcoming')
        past_rental = Rental.objects.filter(seller_id=user.username, rental_status='Past')

        active_buy = Rental.objects.filter(buyer_id=user.username, rental_status='Active')
        upcoming_buy = Rental.objects.filter(buyer_id=user.username, rental_status='Upcoming')
        past_buy = Rental.objects.filter(buyer_id=user.username, rental_status='Past')

        bidding = BotBidding.objects.filter(user=user.username)
        active_buy_array = []
        upcoming_buy_array = []
        past_buy_array = []
        active_rental_array = []
        upcoming_rental_array = []
        past_rental_array = []
        for i in active_rental:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                active_rental_array.append([BotBidding.objects.get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal':
                active_rental_array.append([BotListing.objects.get(pk=i.listing_num),'Normal'])
        for i in upcoming_rental:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                upcoming_rental_array.append([BotBidding.objects.get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal':
                upcoming_rental_array.append([BotListing.objects.get(pk=i.listing_num),'Normal'])
        for i in past_rental:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                past_rental_array.append([BotBidding.objects.get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal':
                past_rental_array.append([BotListing.objects.get(pk=i.listing_num),'Normal'])

        for i in active_buy:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                active_buy_array.append([BotBidding.objects.get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal':
                active_buy_array.append([BotListing.objects.get(pk=i.listing_num),'Normal'])
        for i in active_buy:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                upcoming_buy_array.append([BotBidding.objects.get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal':
                upcoming_buy_array.append([BotListing.objects.get(pk=i.listing_num),'Normal'])
        for i in active_buy:
            rental_from = i.rental_from
            if rental_from == 'Bid':
                past_buy_array.append([BotBidding.objects.get(pk=i.bidding_num),'Bid'])
            if rental_from == 'Normal':
                past_buy_array.append([BotListing.objects.get(pk=i.listing_num),'Normal'])

        # 查询卖家take了哪些bid
        bid_order = BidOrder.objects.filter(seller_id=request.user.username)

        bots = Bot.objects.all()
        trans = Transaction.objects.all()
        context = {
            'bot_list' : bot_list,
            'bots': bots,
            'havebot': havebot,
            'botlisting': botlisting,
            'active_rental': active_rental_array,
            'upcoming_rental': upcoming_rental_array,
            'past_rental': past_rental_array,
            'active_buy': active_buy_array,
            'upcoming_buy': upcoming_buy_array,
            'past_buy': past_buy_array,
            'bid_order': bid_order,
            'bidding': bidding,
            'transactions': trans,
        }

        return render(request, 'mybot.html', context)



