cat << 'EOF' > share_bot.py
import telebot
import os
from flask import Flask
from threading import Thread

TOKEN = "8513371653:AAHNLDy6u0Y3O8b6tF62VwW09gze0q1Kpic"
CHANNEL_ID = -1003986534829
ADMIN_ID = 8119031862

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running 24/7 🚀"

def run_web():
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(commands=['start'])
def start_msg(m):
    text = m.text.split()
    if len(text) > 1:
        msg_id = int(text[1])
        msg = bot.reply_to(m, "⏳ جاري تحضير الملف...")
        try:
            bot.copy_message(m.chat.id, CHANNEL_ID, msg_id)
            bot.delete_message(m.chat.id, msg.message_id)
        except:
            bot.edit_message_text("❌ الملف غير موجود أو تم حذفه.", m.chat.id, msg.message_id)
    else:
        bot.send_message(m.chat.id, "أهلاً بك! هذا البوت مخصص لمشاركة الملفات الكبيرة.\n(للمسؤول: أرسل أي ملف لإنشاء رابط).")

@bot.message_handler(content_types=['document', 'video', 'audio', 'photo'])
def save_file(m):
    if m.chat.id != ADMIN_ID:
        bot.reply_to(m, "⛔ عذراً، لا تمتلك صلاحية رفع الملفات هنا.")
        return
        
    msg = bot.reply_to(m, "⏳ يتم تخزين الملف في المخزن السري...")
    try:
        copied = bot.copy_message(CHANNEL_ID, m.chat.id, m.message_id)
        bot_info = bot.get_me()
        share_link = f"https://t.me/{bot_info.username}?start={copied.message_id}"
        bot.edit_message_text(f"✅ تم التخزين بنجاح!\n\n🔗 رابط المشاركة:\n{share_link}", m.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ! تأكد أن البوت مشرف في القناة.\nالتفاصيل: {e}", m.chat.id, msg.message_id)

print("✅ بوت المشاركة يعمل الآن.. جرب إرسال ملف إليه!")

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling(skip_pending=True)
EOF
python share_bot.py
