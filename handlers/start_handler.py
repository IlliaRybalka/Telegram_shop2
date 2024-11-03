from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Історія покупок"), KeyboardButton("Показати ціни")],
        [KeyboardButton("Меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Handle both message and callback query contexts
    message = update.message or update.callback_query.message
    await message.reply_text(
        'Виберіть опцію або скористайтеся командами з клавіатури:',
        reply_markup=reply_markup
    )
