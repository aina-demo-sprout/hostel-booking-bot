import os
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import db

TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Book a discussion room:\n/rooms - list rooms\n/book <room> <YYYY-MM-DD> <HH:MM>\n/mybookings"
    )


async def rooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\n".join(f"- {r}" for r in db.list_rooms()))


async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        room, day, time = context.args
        slot = datetime.strptime(f"{day} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        await update.message.reply_text("Usage: /book <room> <YYYY-MM-DD> <HH:MM>")
        return
    if db.is_taken(room, slot):
        await update.message.reply_text("Sorry, that slot is taken.")
        return
    db.add_booking(update.effective_user.id, room, slot)
    await update.message.reply_text(f"Booked {room} on {slot:%d %b %H:%M} ✅")


async def my_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = db.bookings_for(update.effective_user.id)
    await update.message.reply_text("\n".join(f"{r} {s}" for r, s in rows) or "No bookings yet.")


def main():
    db.init()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rooms", rooms))
    app.add_handler(CommandHandler("book", book))
    app.add_handler(CommandHandler("mybookings", my_bookings))
    app.run_polling()


if __name__ == "__main__":
    main()
