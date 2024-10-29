from telegram import Update
from telegram.ext import ContextTypes
from handlers.history_handler import view_history
from handlers.show_prices_handler import show_prices
from handlers.start_handler import start

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    if message_text == "Історія покупок":
        await view_history(update, context)
    elif message_text == "Показати ціни":
        await show_prices(update, context)
    elif message_text == "Меню":
        await start(update, context)
    else:
        await update.message.reply_text('Будь ласка, оберіть опцію з меню або скористайтеся кнопками.')
