from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton("Історія покупок"), KeyboardButton("Показати ціни")],
        [KeyboardButton("Меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        'Виберіть опцію або скористайтеся командами з клавіатури:',
        reply_markup=reply_markup
    )
