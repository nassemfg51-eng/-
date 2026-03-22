import telebot
import google.generativeai as genai

# الإعدادات - التوكن والـ API اللي بعتهم
BOT_TOKEN = "8592872662:AAF5lGHEL9OPTMqI94AfM7aiR1W0rpbi5Js"
GEMINI_API_KEY = "AIzaSyCtXs0rC8Vyk27F_WKLXYlF6EV1TiBqUdg"

# إعداد الذكاء الاصطناعي
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

# قاموس لحفظ جلسات الدردشة (الذاكرة)
chat_sessions = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك! أنا بوتك الذكي الخارق، أتحدث العربية وجاهز لخدمتك فوراً. ماذا تريد أن تسأل؟")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.chat.id
    
    # إنشاء جلسة جديدة لو المستخدم أول مرة يكلم البوت
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    
    try:
        # إرسال رسالة "جاري التفكير..." عشان المستخدم يعرف إن البوت شغال
        sent_msg = bot.reply_to(message, "⏳ جارٍ التفكير...")
        
        # الحصول على الرد من Gemini
        response = chat_sessions[user_id].send_message(message.text)
        
        # تعديل رسالة التفكير بالرد النهائي
        bot.edit_message_text(chat_id=user_id, message_id=sent_msg.message_id, text=response.text)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "عذراً، حدث خطأ بسيط. أعد المحاولة.")

print("🚀 البوت انطلق الآن...")
bot.infinity_polling()
