import telebot
from telebot import types
import time
import random
import json
import os

# ================== AYARLAR ==================
TOKEN = os.getenv("TOKEN") or "8944653688:AAGDQhWDQSxNL3qoLD3YAeVKNXyiFw6NEPg"

# Birden fazla admin (DÜZELTİLDİ)
ADMIN_IDS = [8773299135, 8973632679, 8230461239]

bot = telebot.TeleBot(TOKEN)

thomas = ADMIN_IDS   # Eski thomas yerine bunu kullanıyoruz

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
        "*🎉 Merhaba atattv44 #VİZYON oyun Botumuza hoş geldin.*\n\n"
        "*🎯 Başlangıç Hediyesi:* 100000 TL 🏆\n\n"
        "*🎲 Kazanmaya hazır mısın? Komutları dene ve şansını test et!*"
    )

    bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode="Markdown")

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
        "🔹 */gonder <user_id> <miktar>* - 💸 *Belirtilen kullanıcıya belirtilen miktarda para gönderirsiniz.*\n\n"
        "🔹 */kazi* - ⛏️ *Kazı yaparak 0 ile 10 arasında altın bulunur.*\n\n"
        "🔹 */donustur* - 🔄 *Bulunan altınları TL’ye dönüştürür (1 ALTIN = 10000 TL).*\n\n"
        "⚠️ *Dikkat:* *Komutlar arasında 5 saniye beklemelisiniz.*\n"
        "*🎯 İyi şanslar!* 🍀"
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
        "*🎉 Merhaba atattv44 #vizyon oyun Botumuza hoş geldin.*\n\n"
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

@bot.message_handler(commands=['bakiye'])
def bakiyemmvarmi(message):
    user_id = str(message.from_user.id)
    if user_id not in bakiyem:
        bot.reply_to(message, '🛑 Kayıtlı değilsiniz! Lütfen önce /start komutunu kullanın.', parse_mode="Markdown")
        return
    balance = bakiyem[user_id]
    bot.reply_to(message, f"*💰 Güncel Bakiyeniz:* {balance} TL", parse_mode="Markdown")

@bot.message_handler(commands=['risk'])
def risk(message):
    user_id = str(message.from_user.id)
    if flodvarmi(user_id):
        bot.reply_to(message, "*⏳ 5 saniye bekleyin ve tekrar deneyin.*", parse_mode="Markdown")
        return
    if user_id not in bakiyem:
        bot.reply_to(message, '*🛑 Kayıtlı değilsiniz! Lütfen önce /start komutunu kullanın*.', parse_mode="Markdown")
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, '*⚠️ Geçersiz kullanım!*\n\n🔹 *Doğru Kullanım:* /risk 1000', parse_mode="Markdown")
        return
    risk_amount = int(parts[1])
    if risk_amount <= 0:
        bot.reply_to(message, '*⚠️ Paranız 0’dan küçük olamaz!*', parse_mode="Markdown")
        return
    if bakiyem[user_id] < risk_amount:
        bot.reply_to(message, f'*❌ Yetersiz bakiye!*\n\n💰 *Mevcut Bakiye:* {bakiyem[user_id]} *TL*', parse_mode="Markdown")
        return
    if random.random() < 0.7:
        winnings = risk_amount * 2
        bakiyem[user_id] += winnings - risk_amount
        bot.reply_to(message, f'*💰 Kazandınız!* ✅ {winnings} *TL kazandınız.*\n\n💰 *Yeni Bakiye:* {bakiyem[user_id]} *TL*', parse_mode="Markdown")
    else:
        bakiyem[user_id] -= risk_amount
        bot.reply_to(message, f'*💥 Kaybettiniz!* ❌ {risk_amount} *TL kaybettiniz.*\n\n💰 *Yeni Bakiye:* {bakiyem[user_id]} *TL*', parse_mode="Markdown")
    parayi_kaydet_abi()

@bot.message_handler(commands=['puan'])
def puan(message):
    kaydettim(message.from_user.id)
    user_id = str(message.from_user.id)
    
    if user_id not in thomas:
        bot.reply_to(message, '🚫 Bu komutu kullanmaya yetkiniz yok.', parse_mode="Markdown")
        return    
    
    try:
        s = message.text.split()
        if len(s) < 3:
            bot.reply_to(message, "*Kullanım: /puan <kullanıcı_id> <puan>*", parse_mode="Markdown")
            return       

        target_id = str(s[1])
        puan_value = int(s[2])

        bakiyem[target_id] = bakiyem.get(target_id, 0) + puan_value

        parayi_kaydet_abi()
        bot.reply_to(message, f"{target_id} kullanıcısının puanı {puan_value} olarak değiştirildi 🥷🏻💰", parse_mode="Markdown")

    except ValueError:
        bot.reply_to(message, "⚠️ Lütfen geçerli bir sayı girin!", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Beklenmedik bir hata oluştu: {str(e)}", parse_mode="Markdown")

def bakiyedegis(balance):
    if balance >= 1e9:
        return f"{balance / 1e9:.2f} milyar TL"
    elif balance >= 1e6:
        return f"{balance / 1e6:.2f} milyon TL"
    else:
        return f"{balance:.2f} TL"

@bot.message_handler(commands=['zenginler'])
def lider_kim(message):
    kaydettim(message.from_user.id)
    user_id = str(message.from_user.id)
    if flodvarmi(user_id):
        bot.reply_to(message, "𝟓 𝐒𝐚𝐧𝐢𝐲𝐞 𝐛𝐞𝐤𝐥𝐞 𝐭𝐞𝐤𝐫𝐚𝐫 𝐚𝐭.", parse_mode="Markdown")
        return
    sorted_balances = sorted(bakiyem.items(), key=lambda x: x[1], reverse=True)
    leaderboard_message = "🏆 𝐄𝐧 𝐈𝐲𝐢 𝟏𝟎 𝐙𝐞𝐧𝐠𝐢𝐧:\n\n"
    for i, (uid, balance) in enumerate(sorted_balances[:10], start=1):
        try:
            user = bot.get_chat(uid)
            user_name = user.first_name if user.first_name else "Bilinmiyor"
            formatted_balance = bakiyedegis(balance)
            leaderboard_message += f"🎖️ {i}. {user_name} ⇒ {formatted_balance}\n"
        except Exception as e:
            leaderboard_message += f"🎖️ {i}. Bilinmiyor ⇒ {bakiyedegis(balance)}\n"
    bot.reply_to(message, leaderboard_message, parse_mode="Markdown")

@bot.message_handler(commands=['gonder'])
def bakiye_gonder(message):
    kaydettim(message.from_user.id)
    user_id = str(message.from_user.id)
    if user_id not in bakiyem:
        bakiyem[user_id] = 100 
    if message.reply_to_message:
        try:
            parts = message.text.split()
            amount = int(parts[1])  
            target_id = str(message.reply_to_message.from_user.id) 
        except (IndexError, ValueError):
            bot.reply_to(message, '*Lütfen geçerli bir format kullanın. Kullanım: /gonder <miktar>*', reply_to_message_id=message.message_id, parse_mode="Markdown")
            return
    else:
        try:
            parts = message.text.split()
            amount = int(parts[1])  
            target_id = str(parts[2])  
        except (IndexError, ValueError):
            bot.reply_to(message, '*Lütfen geçerli bir format kullanın. Kullanım:* `/gonder <miktar> <user_id>`', reply_to_message_id=message.message_id, parse_mode="Markdown")
            return
    if amount <= 0:
        bot.reply_to(message, '* 0 dan büyük *', reply_to_message_id=message.message_id, parse_mode="Markdown")
        return
    if bakiyem[user_id] < amount:
        bot.reply_to(message, '*Yetersiz bakiye. kardeşim fakirmisin  🥷🏻💰😂*', reply_to_message_id=message.message_id, parse_mode="Markdown")
        return
    bakiyem[user_id] -= amount
    if target_id not in bakiyem:
        bakiyem[target_id] = 100   
    bakiyem[target_id] += amount
    parayi_kaydet_abi()
    bot.reply_to(message, f'*Başarıyla ✅ {target_id} kullanıcısına {amount} TL gönderildi. Yeni bakiye:* {bakiyem[user_id]} *TL*', reply_to_message_id=message.message_id, parse_mode="Markdown")

@bot.message_handler(commands=['bonus'])
def bonus_ver(message):
    user_id = str(message.from_user.id)
    if user_id not in bakiyem:
        bakiyem[user_id] = 100  
    current_time = time.time()
    if user_id in bonus_bakiye:
        time_diff = current_time - bonus_bakiye[user_id]
        if time_diff < 10800:  
            remaining_time = 10800 - time_diff
            remaining_hours = remaining_time // 3600
            remaining_minutes = (remaining_time % 3600) // 60
            bot.reply_to(message, f'*Bonusunuzu almak için {remaining_hours} saat {remaining_minutes} dakika daha beklemeniz gerekiyor😐.*', parse_mode="Markdown")
            return
    bakiyem[user_id] += 500000
    bonus_bakiye[user_id] = current_time  
    parayi_kaydet_abi()
    bot.reply_to(message, f'*Tebrikler ✅ 500,000 TL 💰 bonus kazandınız.\n 💰 Yeni bakiye:* `{bakiyem[user_id]}` *TL*', parse_mode="Markdown")
    
@bot.message_handler(commands=['kayipbonus'])
def bonusabem(message):
    user_id = str(message.from_user.id)    
    if user_id not in thomas:
        bot.reply_to(message, '*Bu komut için yetkin yok. knk*', reply_to_message_id=message.message_id, parse_mode="Markdown")
        return    
    for target_user_id in bakiyem:
        bakiyem[target_user_id] += 300000
    parayi_kaydet_abi()
    bot.reply_to(message, '* Herkese  300,000 TL bonus  gönderildi✅.*', parse_mode="Markdown")

@bot.message_handler(commands=['kazi'])
def kazi(message):
    user_id = str(message.from_user.id)
    
    if user_id not in altinim:
        altinim[user_id] = 0.0
    
    if random.random() < 0.4:
        altin_bul = 0.0
    else:
        altin_bul = round(random.uniform(0, 10), 2)
    altinim[user_id] += altin_bul
    if altin_bul == 0.0:
        response = "*Kazı yaptınız ⛏️ \nAma Altın bulamadınız, tekrar kazmayı deneyin ❌*"
    else:
        response = f"*Kazı yaptınız ⛏️  \n 🥷🏻Maşallah Kral Bu kadar ALTIN  buldun * `{altin_bul} ALTIN` ✅ \n*🎗️ Toplam ALTIN  bakiyeniz:* `{altinim[user_id]} ALTIN`"
    bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['donustur'])
def donustur(message):
    user_id = str(message.from_user.id)
    if user_id not in altinim or altinim[user_id] <= 0:
        bot.reply_to(message, "*Altın bakiyeniz yok. Önce altın kazın!*", parse_mode="Markdown")
        return
    conversion_rate = 10000
    gold_amount = altinim[user_id]
    tl_amount = gold_amount * conversion_rate
    altinim[user_id] = 0
    if user_id not in bakiyem:
        bakiyem[user_id] = 100000
    bakiyem[user_id] += tl_amount
    parayi_kaydet_abi()    
    bot.reply_to(message, f"*Altınlarınız `{gold_amount} ALTIN` TL'ye dönüştürüldü!*\n*Elde edilen TL:* `{tl_amount}` TL\n*Yeni TL bakiyeniz:* `{bakiyem[user_id]}` TL", parse_mode="Markdown")

print("🤖 Bot çalışıyor...")
if __name__=='__main__':
    while True:
        try:
            print("Bot çalışıyor...")
            bot.polling(non_stop=True,timeout=60)
        except Exception as e:
            print(e); time.sleep(3)
