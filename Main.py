import os
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHORTENER_API = os.getenv("SHORTENER_API")
SHORTENER_URL = "https://shrinkme.io/api"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "හයි! 👋 මට වීඩියෝ ලින්ක් එකක් එවන්න. මම ඒක automatic ෂෝට් කරලා දෙන්නම්.")

@bot.message_handler(func=lambda message: True)
def short_link(message):
    user_url = message.text.strip()
    if user_url.startswith("http://") or user_url.startswith("https://"):
        bot.reply_to(message, "පොඩ්ඩක් ඉන්න... ලින්ක් එක හදන ගමන්... ⏳")
        try:
            payload = {'api': SHORTENER_API, 'url': user_url}
            response = requests.get(SHORTENER_URL, params=payload).json()
            if response.get("status") == "success":
                shortened_url = response.get("shortenedUrl")
                bot.send_message(message.chat.id, f"✅ මෙන්න ඔයාගේ ලින්ක් එක:\n\n{shortened_url}")
            else:
                bot.send_message(message.chat.id, "❌ ලින්ක් එක හදන්න බැරි වුණා.")
        except Exception as e:
            bot.send_message(message.chat.id, "⚠️ පද්ධතියේ දෝෂයක්.")
    else:
        bot.reply_to(message, "වලංගු ලින්ක් එකක් එවන්න. 🛑")

bot.infinity_polling()
