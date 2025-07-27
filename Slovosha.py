from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import word_analyzer

TOKEN = "token has been removed!!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! You are using «словоша», a Russian helper bot.\nSend me a Russian word."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_word = update.message.text.strip()
    russian_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    is_russian = all(char in russian_letters for char in user_word)

    if is_russian:
        analysis = word_analyzer.analyze_word(user_word)
        if len(analysis) <= 4096:
            await update.message.reply_text(analysis)
        else:
            # this part is for long time error from telegram
            for i in range(0, len(analysis), 4096):
                await update.message.reply_text(analysis[i:i+4096])
    else:
        await update.message.reply_text("❗ Please send a valid Russian word (Cyrillic only).")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
