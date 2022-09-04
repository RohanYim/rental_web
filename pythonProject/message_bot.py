import websocket  # pip install websocket-client
import json
import threading
import time
import datetime
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
from websocket._exceptions import WebSocketConnectionClosedException
import urllib

## webhook-url
# balko
balko_success = 'https://discord.com/api/webhooks/870957941451276298/LUEoCP0iIYzo25L3gC-wikbr1rfopIozf6G9BN30pGJniLlSByz3ZudXecE6_XUWiE28'
balko_announcement = 'https://discord.com/api/webhooks/871216896446447616/1uu-BR4TYK5mGRaGRvEqUJXkQlk0NcigVB-oFDjx1Na6xhu38CH4ZIHx7K9Aqlroc5NZ'
balko_update = 'https://discord.com/api/webhooks/874946296451067914/-9D0kAup9NLrazDonqK3AXH7cdPXbgHgvFKpQE2LN34fBKDXT0Mf8pxhgfE-OZ_RuTW0'
# prism
prism_update = 'https://discord.com/api/webhooks/875230088524857375/ZHL3t_QUj4V5ItjMINlW0f5LIwf_YWS1OCJZXcWUmKPf1_Qo2rfrTZk6k6_x5aORn-fG'
prism_announcement = 'https://discord.com/api/webhooks/876024598267854848/nZbVysob6nMDdffirBeuRrmwzFTyjOt3kFep5zXn7HWNZZnc49dsDqVlvJVFz8yKCxkP'
prism_success = 'https://discord.com/api/webhooks/876024630085816370/tyfoIXXXhhjL8Mg22Nzi56d1Ckt6VjSW54oDQHvTBBxCFQXHARHcw1bgBabz60hpIxPk'
# reaio
reaio_update = 'https://discord.com/api/webhooks/875229794609037373/IkI8ZvbHDiY3pAxcIKGyDmB7PIpq80LCXN3yS8HGgsGuGy_jZI9Fo-uT1CCMk9tNwydh'
reaio_announcement = 'https://discord.com/api/webhooks/876023949140557874/txVXMQUEKmLHWeoHmIAI3IcBhNg8a2Hmzw8Jp4qMemqsXw9kZcUCEnL7vXtG3bZiKaOh'
reaio_success = 'https://discord.com/api/webhooks/876024429610668052/yZPJEJTz_Xa9ZAq4Q4ededepgM-y10BlU4PvUk9XrD8ePTnHFzIjtwdIo5zjCQaCxJS6'
# mekaio
mekaio_update = 'https://discord.com/api/webhooks/875558290652823562/tSshvMUgAwfpw2fnLDn8V15rAXJMf02Y_1C0ZZgO3EAJTziX-jSLM1mdVBV7YTL-Y50T'
mekaio_announcement = 'https://discord.com/api/webhooks/876024697937068032/nHK5mAxbQOPE7dVocPsjqJfHzt0ocXjyb2q-uJetuKBeX2l7ppFz9vV4-kVc8724Fgbp'
mekaio_success = 'https://discord.com/api/webhooks/876024726525452288/ri3fgRm_bBzgJg62Laxdlj0ZBbv0VABok1Cz5ZdIZ2_6hHNe6XhAMuPOnCVtcbnEcoy1'
# easycop
easycop_update = 'https://discord.com/api/webhooks/875558575588659211/tJXzrufu14xa1EdmxZEFGd1qXNzwHzaqW8ompLPLCIijYzRL7VlZCSYscBC9B39h0MWJ'
easycop_announcement = 'https://discord.com/api/webhooks/876024980033384448/3hoSKW2BzNdynCNPlRuuF4C_6uo_Iasx1z1EWgB04rN994-He1zRRkDjxIo8CRFj2Fnp'
easycop_success = 'https://discord.com/api/webhooks/876025013109665812/96Vb7vLGhWaYZrE0HGT1kUPFYtV9PuUy1lLPvjUC_zdI_uj9d17JuNKPlbCgSSPMN2rK'
# kylin
kylin_update = 'https://discord.com/api/webhooks/875558363033903155/3rShMTcsWXhklQBjeNRWUSaMf5I_HS-ah66Qta5G147x-zz6poCEfGmJbMQJPJcpP7B5'
kylin_announcement = 'https://discord.com/api/webhooks/876024789553254400/eSXJWM4H_vl3skBBk2gsSw6SsvktVJUxieSim1PRRfay0zXeHtzUOdWSirRRwYZfxQgY'
kylin_success = 'https://discord.com/api/webhooks/876024819932610601/kU-Chu7fWN2p3aoDFov9lj1mWzZpDhTqJRi6hmZQqzK_wunVl6oR03nLpd8bqE14NbR5'
# nsb
nsb_update = 'https://discord.com/api/webhooks/875558496035287091/r3hP3hAULghNrdSLEQ8R18k_iy55bZIwL45tLxHrDjwwD3SB-JBEtMf9aF4pNQ_e3wYW'
nsb_announcement = 'https://discord.com/api/webhooks/876024884604600371/cK7De5c2X3o4usbcCXCiZNLl_RG6I1FYZPiBkf9j-4V5QTmzzqk6g7P9obPeK-NbadWJ'
nsb_success = 'https://discord.com/api/webhooks/876024912219881533/RlqTgorQVMQgPvevqdnK8SXKDXOIsMkXsqPXoZ2ab-luQwAqbUPSfEdRdsydiWkjHWnt'
# phantom
phantom_update = ''
phantom_announcement =''
phantom_success =''
# wrath
wrath_update = ''
wrath_announcement =''
wrath_success =''
# pd
pd_update = ''
pd_announcement =''
pd_success =''
# sole
sole_update = ''
sole_announcement =''
sole_success =''
# kodai
kodai_update = ''
kodai_announcement =''
kodai_success =''
# wrath
wrath_update = ''
wrath_announcement =''
wrath_success =''

## embed-info
embed_footer = "1024 Rental | Powered by YIM"
embed_icon = 'https://www.whop.io/assets/whop.png'
embed_color = 0x82111f

## channels
general_announcement = '805864705008599070'
other_aio_bots = '771200794615742485'
king_aio_bots = '771200643255500880' # kodai,wrath,ganesh
supreme_bots = '771200619046240256'

balko_success_channel = '771202208616284180'
prism_success_channel = '771202034086707210'
reaio_success_channel = '771202146153660418'
easycop_success_channel = '868025676106694677'  # cloud
mekaio_success_channel = '791113430076489768'
kylin_success_channel = '785656724174143508'
nsb_success_channel = '833730041568297020'    # ad

success_channels = [balko_success_channel, prism_success_channel, reaio_success_channel, easycop_success_channel,
                    mekaio_success_channel, kylin_success_channel, nsb_success_channel]




def send_json_request(ws, request):
    ws.send(json.dumps(request))


def recieve_json_response(ws):
    try:
        response = ws.recv()
    except (WebSocketConnectionClosedException, ConnectionResetError):
        print("Caught Connection Error")
        time.sleep(5)
        return 0
    else:
        if response:
            return json.loads(response)


def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print(str(datetime.datetime.now()) + ": " + "Heartbeat sent")


def connect():
    temp = 0
    while temp <= 5:
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
        event = recieve_json_response(ws)
        if event == 0:
            temp = temp + 1
        else:
            temp = 6
    heartbeat_interval = event['d']['heartbeat_interval'] / 1000
    threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

    token = 'mfa.lFc0VdyG50_6MchMsovHneXDaAfbIKpikm-KfyAEdZr_fyPvOLtWgQH5XTXzpwRrmfz_VfjUgCFrkY70LGsx'
    payload = {
        'op': 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "windows",
                "$browser": "chrome",
                "$device": 'pc'
            }
        }
    }
    send_json_request(ws, payload)
    return ws, event


ws, event = connect()

while True:
    event = recieve_json_response(ws)
    if event == 0:
        print("Connecting...")
        ws, event = connect()

    if event is None:
        continue
    if ('d' in event) and (event['d'] is None):
        continue
    try:
        ## bot-success
        if ('channel_id' in event['d']) and (str(event['d']['channel_id']) in success_channels):
            if ('embeds' in event['d']) and (len(event['d']['embeds']) != 0):
                embed = event['d']['embeds'][0]
                if event['d']['channel_id'] == balko_success_channel:
                    webhook_url = balko_success
                elif event['d']['channel_id'] == prism_success_channel:
                    webhook_url = prism_success
                elif event['d']['channel_id'] == nsb_success_channel:
                    webhook_url = nsb_success
                elif event['d']['channel_id'] == easycop_success_channel:
                    webhook_url = easycop_success
                elif event['d']['channel_id'] == kylin_success_channel:
                    webhook_url = kylin_success
                elif event['d']['channel_id'] == mekaio_success_channel:
                    webhook_url = mekaio_success
                elif event['d']['channel_id'] == reaio_success_channel:
                    webhook_url = reaio_success
                else:
                    webhook_url = 'https://discord.com/api/webhooks/861786508825853993/UIGF2asljMIhmQPb8ASELLqt94xnTNPe3fpIuWHDdNv1hqcoG0UO9nkSmJD5XgYzJ-yM'

                embed['footer']['text'] = embed_footer
                embed['footer']['icon_url'] = embed_icon
                embed['color'] = embed_color
                # embed.set_footer(text="Thanks for using HR Space", icon_url="https://www.whop.io/assets/whop.png")
                webhook = DiscordWebhook(
                    url=webhook_url)

                webhook.add_embed(embed)
                response = webhook.execute()

                print(str(datetime.datetime.now()) + ": " + "webhook sent")
            else:
                embed = event['d']['content']
                webhook_url = balko_success
                webhook = DiscordWebhook(
                    url=webhook_url, content=embed)

                response = webhook.execute()

                print(str(datetime.datetime.now()) + ": " + "webhook sent")

        ## bot-announcement
        elif ('channel_id' in event['d']) and (str(event['d']['channel_id']) == general_announcement):
            if ('embeds' in event['d']) and (len(event['d']['embeds']) != 0):
                embed = event['d']['embeds'][0]
                print(embed)
                if embed['author']['name'] == 'BALKO':
                    embed['author']['name'] = 'Balko announcement'
                    webhook_url = balko_announcement
                elif embed['author']['name'] == 'PRISM':
                    embed['author']['name'] = 'Prism announcement'
                    webhook_url = prism_announcement
                elif embed['author']['name'] == 'NSB':
                    embed['author']['name'] = 'Nsb announcement'
                    webhook_url = nsb_announcement
                elif embed['author']['name'] == 'EASYCOP':
                    embed['author']['name'] = 'Easycop announcement'
                    webhook_url = easycop_announcement
                elif embed['author']['name'] == 'KYLIN':
                    embed['author']['name'] = 'Kylin announcement'
                    webhook_url = kylin_announcement
                elif embed['author']['name'] == 'MEKAIO':
                    embed['author']['name'] = 'Mekaio announcement'
                    webhook_url = mekaio_announcement
                elif embed['author']['name'] == 'REAIO':
                    embed['author']['name'] = 'Reaio announcement'
                    webhook_url = reaio_announcement
                else:
                    webhook_url = 'https://discord.com/api/webhooks/861786508825853993/UIGF2asljMIhmQPb8ASELLqt94xnTNPe3fpIuWHDdNv1hqcoG0UO9nkSmJD5XgYzJ-yM'

                embed['footer']['text'] = embed_footer
                embed['footer']['icon_url'] = embed_icon
                embed['color'] = embed_color

                webhook = DiscordWebhook(
                    url=webhook_url)

                webhook.add_embed(embed)
                response = webhook.execute()

                print(str(datetime.datetime.now()) + ": " + "webhook sent")

        ## bot-update
        elif ('channel_id' in event['d']) and (str(event['d']['channel_id']) == other_aio_bots):
            # print(len(event['d']['embeds']))
            if ('embeds' in event['d']) and (len(event['d']['embeds']) != 0):
                embed = event['d']['embeds'][0]
                print(embed)
                if embed['author']['name'] == 'BALKO UPDATE':
                    embed['author']['name'] = 'Balko update'
                    webhook_url = balko_update
                elif embed['author']['name'] == 'REAIO UPDATE':
                    embed['author']['name'] = 'Reaio update'
                    webhook_url = reaio_update
                elif embed['author']['name'] == 'PRISM UPDATE':
                    embed['author']['name'] = 'Prism update'
                    webhook_url = prism_update
                elif embed['author']['name'] == 'MEKAIO UPDATE':
                    embed['author']['name'] = 'Mekaio update'
                    webhook_url = mekaio_update
                elif embed['author']['name'] == 'KYLIN UPDATE':
                    embed['author']['name'] = 'Kylin update'
                    webhook_url = kylin_update
                elif embed['author']['name'] == 'NSB UPDATE':
                    embed['author']['name'] = 'Nsb update'
                    webhook_url = nsb_update
                elif embed['author']['name'] == 'EASYCOP UPDATE':
                    embed['author']['name'] = 'Easycop update'
                    webhook_url = easycop_update
                else:
                    webhook_url = 'https://discord.com/api/webhooks/861786508825853993/UIGF2asljMIhmQPb8ASELLqt94xnTNPe3fpIuWHDdNv1hqcoG0UO9nkSmJD5XgYzJ-yM'

                embed['footer']['text'] = embed_footer
                embed['footer']['icon_url'] = embed_icon
                embed['color'] = embed_color

                webhook = DiscordWebhook(
                    url=webhook_url)

                webhook.add_embed(embed)
                response = webhook.execute()

                print(str(datetime.datetime.now()) + ": " + "webhook sent")
            else:
                embed = event['d']['content']
                webhook_url = 'https://discord.com/api/webhooks/871216896446447616/1uu-BR4TYK5mGRaGRvEqUJXkQlk0NcigVB-oFDjx1Na6xhu38CH4ZIHx7K9Aqlroc5NZ'
                webhook = DiscordWebhook(
                    url=webhook_url, content=embed)

                response = webhook.execute()

                print(str(datetime.datetime.now()) + ": " + "webhook sent")
        else:
            pass

        op_code = event['op']
        if op_code == 11:
            print('heartbeat received')
    except:
        pass

