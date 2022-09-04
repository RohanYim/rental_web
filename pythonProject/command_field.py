import requests
import configparser
import os
import sys

# order_number = sys.argv[1]
# command = sys.argv[2]

def command_field(order_number, command, use):
    if use == 'order':
        CONFIG_FILE = "order_config.cfg"
        if os.path.exists(os.path.join(os.getcwd(), CONFIG_FILE)):
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)

            Bot = config.get(order_number, "Bot")
            if Bot == 'Velox':
                auto_reset = "!reset_command %(Bot)s %(Key)s %(Key_nickname)s %(Seller)s <@%(Seller)s>"
                config.set(order_number, "auto_reset", auto_reset)
            if Bot == 'Balko':
                auto_reset = "!reset_command %(Bot)s %(Key)s %(Key_nickname)s %(Seller)s <@%(Seller)s>"
                config.set(order_number, "auto_reset", auto_reset)
            if Bot == 'Mekaio':
                auto_reset = "!reset_command %(Bot)s %(Key)s %(Key_nickname)s %(Seller)s <@%(Seller)s>"
                config.set(order_number, "auto_reset", auto_reset)
            if Bot == 'Stellar':
                auto_reset = "!reset_command %(Bot)s %(Key)s %(Key_nickname)s %(Seller)s <@%(Seller)s>"
                config.set(order_number, "auto_reset", auto_reset)
            if Bot == 'Kodai':
                auto_reset = "!reset_command %(Bot)s %(Key)s %(Key_nickname)s %(Seller)s <@%(Seller)s>"
                config.set(order_number, "auto_reset", auto_reset)
            if Bot == 'Koi':
                auto_reset = "!reset_command %(Bot)s %(Key)s %(Key_nickname)s %(Seller)s <@%(Seller)s>"
                config.set(order_number, "auto_reset", auto_reset)
            with open('config.cfg', 'w') as configfile:
                config.write(configfile)
            # Key = config.get(order_number, "Key")
            # Key_nickname = config.get(order_number, "Key_nickname")
            # Start_time = config.get(order_number, "Start_time")
            # End_time = config.get(order_number, "End_time")
            # Reset_time = config.get(order_number, 'Reset_time')
            # Buyer = config.get(order_number, "Buyer")
            # Seller = config.get(order_number, "Seller")
            Order_buyer = config.get(order_number, "Order_buyer")
            Order_seller = config.get(order_number, "Order_seller")
            Reset_buyer = config.get(order_number, "Reset_buyer")
            Reset_seller = config.get(order_number, "Reset_seller")
            Reset_cancel_seller = config.get(order_number, "Reset_cancel_seller")
            End_buyer = config.get(order_number, "End_buyer")
            End_seller = config.get(order_number, "End_seller")
            auto_reset = config.get(order_number, "auto_reset")
            cancel_buyer = config.get(order_number, "cancel_buyer")
            cancel_seller = config.get(order_number, "cancel_seller")
            Start_seller = config.get(order_number, "start_seller")
            Start_buyer = config.get(order_number, "start_buyer")
            # values_query2 = config.get(order_number, "values_query2")
    elif use == 'payout':
        PAYOUT_CONFIG_FILE = "payout_config.cfg"
        if os.path.exists(os.path.join(os.getcwd(), PAYOUT_CONFIG_FILE)):
            config = configparser.ConfigParser()
            config.read(PAYOUT_CONFIG_FILE)

            payout_request = config.get(order_number, "payout_request")
            payout_denied = config.get(order_number, "payout_denied")
            payout_succeed = config.get(order_number, "payout_succeed")
    elif use == 'key':
        KEYCHECK_CONFIG_FILE = "keycheck_config.cfg"
        if os.path.exists(os.path.join(os.getcwd(), KEYCHECK_CONFIG_FILE)):
            config = configparser.ConfigParser()
            config.read(KEYCHECK_CONFIG_FILE)
            keycheck_reset = config.get(order_number, "keycheck_reset")
            keycheck_fail = config.get(order_number, "keycheck_fail")
            keycheck_success = config.get(order_number, "keycheck_success")

    if command == 'order_buyer':
        content = Order_buyer
    if command == 'order_seller':
        content = Order_seller
    if command == 'reset_buyer':
        content = Reset_buyer
    if command == 'reset_seller':
        content = Reset_seller
        if Bot == 'Velox':
            content = auto_reset
        if Bot == 'Balko':
            content = auto_reset
        if Bot == 'Mekaio':
            content = auto_reset
        if Bot == 'Stellar':
            content = auto_reset
        if Bot == 'Kodai':
            content = auto_reset
        if Bot == 'Koi':
            content = auto_reset
    if command == 'reset_cancel_seller':
        content = Reset_cancel_seller
    if command == 'end_buyer':
        content = End_buyer
    if command == 'end_seller':
        content = End_seller
    if command == 'start_seller':
        content = Start_seller
    if command == 'start_buyer':
        content = Start_buyer
    if command == 'cancel_buyer':
        content = cancel_buyer
    if command == 'cancel_seller':
        content = cancel_seller
    if command == 'payout_request':
        content = payout_request
    if command == 'payout_denied':
        content = payout_denied
    if command == 'payout_succeed':
        content = payout_succeed
    if command == 'keycheck_reset':
        content = keycheck_reset
    if command == 'keycheck_success':
        content = keycheck_success
    if command == 'keycheck_fail':
        content = keycheck_fail

    payload = {
        'content': content
    }

    header = {
        'authorization': 'NzQwNDcxMzUxNTQ1OTU0NDQ2.YOqm0A.Awavde7lwPhZp57S6BpuWWMIE-8'
    }

    r = requests.post('https://discord.com/api/v8/channels/850597103783641131/messages', data=payload, headers=header)
