import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread
import os

# 1. الإعدادات الخاصة بك (تم التحديث بالمفتاح الجديد)
BOT_TOKEN = "8592872662:AAF5lGHEL9OPTMqI94AfM7aiR1W0rpbi5Js"
GEMINI_API_KEY = "AIzaSyCzC7UAQFXdW8tLq04gdus_xHqqTrWRHtg"

# 2. تشغيل سيرفر بسيط (عشان الاستضافة المجانية متقفلش البوت)
app = Flask('')
@app.route('/')
def home():
    return "البوت شغال بأعلى كفاءة 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

# 3. إعداد الذكاء الاصطناعي (Gemini)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

# 4. معالجة الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # إرسال حالة "جاري الكتابة" في تلجرام
        bot.send_chat_action(message.chat.id, 'typing')
        
        # طلب الرد من الذكاء الاصطناعي
        response = model.generate_content(message.text)
        
        # الرد على المستخدم
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "يا بطل، حصل ضغط بسيط.. جرب تبعت رسالتك تاني.")

# 5. انطلاق البوت
def start_bot():
    print("🚀 البوت انطلق الآن...")
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل السيرفر والبوت مع بعض في نفس الوقت
    t = Thread(target=run)
    t.start()
    start_bot()
