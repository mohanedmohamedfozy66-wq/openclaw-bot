import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MODEL = "minimax/minimax-m2.5:free"

chat_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا مساعدك الذكي 🤖")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_message = update.message.text

    if chat_id not in chat_histories:
        chat_histories[chat_id] = [
            {"role": "system", "content": "أنت مساعد ذكي ومفيد."}
        ]

    chat_histories[chat_id].append({"role": "user", "content": user_message})

    if len(chat_histories[chat_id]) > 20:
        system = chat_histories[chat_id][0]
        chat_histories[chat_id] = [system] + chat_histories[chat_id][-19:]

    response = None
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://telegram-bot.app",
                "X-Title": "Telegram AI Bot"
            },
            json={
                "model": MODEL,
                "messages": chat_histories[chat_id]
            },
            timeout=30
        )
        data = response.json()
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
            chat_histories[chat_id].append({"role": "assistant", "content": reply})
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text(f"خطأ: {str(data)}")
    except Exception as e:
        msg = f"خطأ: {str(e)}"
        if response is not None:
            msg += f"\n{response.text[:200]}"
        await update.message.reply_text(msg)

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_histories[chat_id] = []
    await update.message.reply_text("تم مسح المحادثة! 🗑️")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()                "messages": chat_histories[chat_id]
            }
        )
        reply = response.json()["choices"][0]["message"]["content"]
        chat_histories[chat_id].append({
            "role": "assistant",
            "content": reply
        })
        await update.message.reply_text(reply)
    except requests.exceptions.Timeout:
    await update.message.reply_text("timeout - النموذج بطيء")
except Exception as e:
    error_msg = f"خطأ: {str(e)}"
    if response:
        error_msg += f"\nResponse: {response.text[:200]}"
    await update.message.reply_text(error_msg)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
