import telebot
from telebot import types
import time
import random
import json
import os

# ================== AYARLAR ==================
TOKEN = os.getenv("TOKEN") or "8944653688:AAGDQhWDQSxNL3qoLD3YAeVKNXyiFw6NEPg"

# Birden fazla admin ekleyebilirsiniz
ADMIN_IDS = [8773299135, 8973632679, 8230461239]   # Buraya istediğin kadar ID ekle

bot = telebot.TeleBot(TOKEN)

param = 'balances.json'
kullanici_abelerim = 'users.txt'

bakiyem = {}
ensoneyebastin = {}
bonus_bakiye = {}
altinim = {}

def bakiyeyebak():
    try:
        with open(param, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def parayi_kaydet_abi():
    with open(param, 'w') as f:
        json.dump(bakiyem, f, indent=4)

def kaydettim(user_id):
    with open(kullanici_abelerim, 'a+') as f:
        f.seek(0)
        if str(user_id) not in f.read():
            f.write(f"{user_id}\n")

def flodvarmi(user_id):
    now = time.time()
    if user_id in ensoneyebastin:
        time_diff = now - ensoneyebastin[user_id]
        if time_diff < 1:  
            return True
    ensoneyebastin[user_id] = now
    return False

def logkontrol(user_id):
    print(f"[LOG] Kullanıcı {user_id} komut kullandı.")

def is_admin(user_id):
    return user_id in ADMIN_IDS

bakiyem = bakiyeyebak()

# ================== START ==================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if flodvarmi(user_id):
        bot.reply_to(message, '⚠️ Flood yapma! 1 saniyede 1 istek yapabilirsin.', parse_mode="Markdown")
        return    
    kaydettim(user_id)
    logkontrol(user_id)
    if user_id not in bakiyem:
        bakiyem[user_id] = 100000
        parayi_kaydet_abi()  

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("👤 Sahibim", url="https://t.me/alonehazretleri"),
        types.InlineKeyboardButton("📢 Kanal", url="https://t.me/alonetools"),
        types.InlineKeyboardButton("👤 Gruplar", url="https://t.me/atattv44vizyon")
    )
    markup.row(types.InlineKeyboardButton("📖 Komutlar", callback_data="komutlar"))
    markup.add(types.InlineKeyboardButton("➕ Beni Gruba Ekle", url="https://t.me/atattv44oyunbot?startgroup=new"))

    photo_url = 'https://r.resimlink.com/qRPiMK67Bjg.jpg'
    caption = (
        "*🎉 Merhaba usom oyun Botumuza hoş geldin.*\n\n"
        "*🎯 Başlangıç Hediyesi:* 100000 TL 🏆\n\n"
        "*🎲 Kazanmaya hazır mısın? Komutları dene ve şansını test et!*"
    )

    bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode="Markdown")

# ================== KOMUTLAR ==================
@bot.callback_query_handler(func=lambda call: call.data == "komutlar")
def show_commands(call):
    commands_text = (
        "*📖 Kumar Botu Komutları:*\n\n"
        "🔹 */start* - 🎉 *Botu başlatır ve 100.000 TL bakiye verir.*\n"
        "🔹 */bakiye* - 💰 *Güncel bakiyenizi gösterir.*\n"
        "🔹 */risk <miktar>* - 🎲 *Belirtilen miktarı riske atar.*\n"
        "   └ 💡 *%50 kazanma şansı:*\n"
        "     ◦ *Kazanırsanız 2 katını alırsınız.*\n"
        "     ◦ *Kaybederseniz tüm parayı kaybedersiniz.*\n\n"
        "🔹 */zenginler* - 🏆 *En zengin kullanıcıları gösterir.*\n\n"
        "🔹 */bonus* - 🎁 *Günlük 500,000 TL bonus alırsınız.*\n\n"
        "🔹 */gonder <user_id> <miktar>* - 💸 *Belirtilen kullanıcıya para gönderirsiniz.*\n\n"
        "🔹 */kazi* - ⛏️ *Kazı yaparak altın bulunur.*\n\n"
        "🔹 */donustur* - 🔄 *Altınları TL'ye dönüştürür.*\n\n"
        "⚠️ *Dikkat:* Komutlar arasında 5 saniye beklemelisiniz."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Geri", callback_data="geri"))

    bot.edit_message_caption(
        caption=commands_text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data == "geri")
def go_back(call):
    caption = (
        "*🎉 Merhaba usom oyun Botumuza hoş geldin.*\n\n"
        "*🎯 Başlangıç Hediyesi:* 100000 TL 🏆\n\n"
        "*🎲 Kazanmaya hazır mısın? Komutları dene ve şansını test et!*"
    )

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("👤 Sahibim", url="https://t.me/alonehazretleri"),
        types.InlineKeyboardButton("📢 Kanal", url="https://t.me/alonetools"),
        types.InlineKeyboardButton("👤 Gruplar", url="https://t.me/atattv44vizyon")
    )
    markup.row(types.InlineKeyboardButton("📖 Komutlar", callback_data="komutlar"))
    markup.add(types.InlineKeyboardButton("➕ Beni Gruba Ekle", url="https://t.me/atattv44oyunbot?startgroup=new"))

    bot.edit_message_caption(
        caption=caption,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ================== DİĞER KOMUTLAR (Aynı kaldı) ==================
# ... (kodunun geri kalanı aynı)

print("🤖 Bot çalışıyor...")
if __name__=='__main__':
    while True:
        try:
            print("Bot çalışıyor...")
            bot.polling(non_stop=True, timeout=60)
        except Exception as e:
            print(e)
            time.sleep(3)
