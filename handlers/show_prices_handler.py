from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from constants import PRODUCT_CHOICES

async def show_prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    options = [
        (f"{info['name']} - {info['price']}", key) for key, info in PRODUCT_CHOICES.items()
    ]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Оберіть продукт з ціною:', reply_markup=reply_markup)
