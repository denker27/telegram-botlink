from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Ambil token dari Railway Environment Variable
TOKEN = os.getenv("8135110264:AAHnp_rb3b_uc8_25w9fj0FAXlA2THpI78Q")

# Baca semua link dari file
with open("links.txt", "r") as f:
    group_links = [line.strip() for line in f.readlines()]

# Simpan posisi per user (untuk tracking link ke berapa)
user_positions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_positions[chat_id] = 0
    await send_link(update, chat_id)

async def next_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_positions[chat_id] = user_positions.get(chat_id, 0) + 1
    await send_link(update, chat_id)

async def send_link(update, chat_id):
    pos = user_positions[chat_id]
    if pos >= len(group_links):
        await update.message.reply_text("✅ Semua link sudah dibagikan.")
        return
    link = group_links[pos]
    await update.message.reply_text(f"Link grup ke-{pos+1}:\n{link}")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("next", next_link))
    app.run_polling()
