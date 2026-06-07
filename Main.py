import os
import requests
import telebot

# Environment Variables වලින් දත්ත ලබා ගැනීම (Koyeb එකේදී අපි මේවා සෙට් කරනවා)
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHORTENER_API = os.getenv("SHORTENER_API")
SHORTENER_URL = "https://shrinkme.io/api"

bot = telebot.TeleBot(BOT_TOKEN)

# යූසර් /start කරපුහම ලැබෙන මැසේජ් එක
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "හයි! 👋 ටෙලිග්‍රෑම් වීඩියෝ ෂෙයාරින් බොට් වෙත සාදරයෙන් පිළිගනිමු.\n\n"
        "ඔයාට ඇඩ් ලින්ක් එකක් බවට පත් කරන්න ඕනේ වීඩියෝ ලින්ක් එක (TeraBox, Mega, Google Drive හෝ වෙනත් ඕනෑම ලින්ක් එකක්) මට එවන්න. "
        "මම ඒක automatic ෂෝට් කරලා දෙන්නම්. 🌐"
    )
    bot.reply_to(message, welcome_text)

# යූසර් ලින්ක් එකක් එව්වහම ක්‍රියාත්මක වන කොටස
@bot.message_handler(func=lambda message: True)
def short_link(message):
    user_url = message.text.strip()
    
    # මැසේජ් එක ලින්ක් එකක්ද කියලා පරික්ෂා කිරීම
    if user_url.startswith("http://") or user_url.startswith("https://"):
        bot.reply_to(message, "පොඩ්ඩක් ඉන්න... ඔයාගේ වීඩියෝ ලින්ක් එක ඇඩ් ලින්ක් එකක් බවට පත් කරන ගමන්... ⏳")
        
        try:
            # ShrinkMe API එකට රික්වෙස්ට් එක යැවීම
            payload = {'api': SHORTENER_API, 'url': user_url}
            response = requests.get(SHORTENER_URL, params=payload).json()
            
            if response.get("status") == "success":
                shortened_url = response.get("shortenedUrl")
                
                success_message = (
                    "✅ **මෙන්න ඔයාගේ ඇඩ් ලින්ක් එක සූදානම්!**\n\n"
                    f"`{shortened_url}`\n\n"
                    "💡 **යූසර්ස්ලාට බලන්න දෙන්න ඕනේ මේ ලින්ක් එක.** ඔවුන් මේ ලින්ක් එකට ගිහින් ඇඩ් එක බැලුවට පස්සේ "
                    "ඔයා දාපු ඔරිජිනල් වීඩියෝ එකට automatic එකතු වෙනවා. ඔයාට ඒකෙන් මුදල් උපයන්න පුළුවන්!"
                )
                bot.send_message(message.chat.id, success_message, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "❌ ලින්ක් එක සාදා ගැනීමට නොහැකි වුණා. කරුණාකර API Key එක පරික්ෂා කරන්න.")
        
        except Exception as e:
            bot.send_message(message.chat.id, "⚠️ පද්ධතියේ දෝෂයක් සිදු වුණා. පසුව උත්සාහ කරන්න.")
    else:
        bot.reply_to(message, "කරුණාකර වලංගු වීඩියෝ හෝ ෆයිල් HTTP/HTTPS ලින්ක් එකක් පමණක් එවන්න. 🛑")

# බොට් එක දිගටම වැඩ කරන්න
bot.infinity_polling()
