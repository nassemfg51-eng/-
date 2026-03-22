import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. إعداد المحرك الجبار (Gemini)
# تم وضع المفتاح الخاص بك هنا
genai.configure(api_key="AIzaSyCgz1K1olooSe2E7oagBiCzDhydu7st9rY")

# تخصيص الإعدادات لسرعة الرد ودقة اللغة العربية
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # إصدار فلاش هو الأسرع على الإطلاق (طلقة)
    generation_config=generation_config,
    system_instruction="أنت مساعد ذكي خارق تتحدث اللغة العربية فقط بأسلوب فصيح وواضح. ردودك سريعة ومختصرة وذكية جداً. ممنوع استخدام أي لغة أخرى غير العربية."
)

# 2. سيرفر Flask (لضمان عمل الاستضافة 24/7)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online"
@app.route('/api/alive')
def alive(): return "OK"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 3. معالجة الرسائل بذكاء وسرعة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # إرسال النص للمحرك والحصول على رد
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("عذراً، حدث خطأ بسيط. أعد المحاولة.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أنا بوتك الذكي الخارق، أتحدث العربية فقط وجاهز لخدمتك فوراً. ماذا تريد أن تسأل؟")

if __name__ == '__main__':
    # تشغيل السيرفر في الخلفية
    Thread(target=run_flask).start()
    
    # 4. تشغيل البوت (التوكن الخاص بك)
    token = "8592872662:AAECUGKqAeiWSGj2ChUQgkdk71gRbVwW8Ys"
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("البوت انطلق الآن..")
    application.run_polling()
