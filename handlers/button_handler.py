from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from constants import PRODUCT_CHOICES
from handlers.purchase_handler import handle_purchase
from handlers.show_prices_handler import show_prices
from handlers.start_handler import start

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    await query.answer()

    if data.startswith('buy_'):
        product_choice = data[4:]
        await handle_purchase(update, context, product_choice)
    elif data == 'back':
        await show_prices(update, context)
    elif data == 'back_to_menu':
        await start(update, context)
    elif data in PRODUCT_CHOICES:
        selected = PRODUCT_CHOICES[data]
        text = f"Ви вибрали {selected['name']}. Ціна: {selected['price']}\n\n{selected['description']}"
        keyboard = [
            [InlineKeyboardButton("Купити", callback_data=f'buy_{data}')],
            [InlineKeyboardButton("Назад", callback_data='back')],
            [InlineKeyboardButton("Меню", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await query.answer('Невідома команда')
