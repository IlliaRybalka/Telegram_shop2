from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime
from constants import PRODUCT_CHOICES
from database import db

async def handle_purchase(update: Update, context: CallbackContext, product_choice: str) -> None:
    user_id = update.callback_query.from_user.id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if product_choice in PRODUCT_CHOICES:
        selected = PRODUCT_CHOICES[product_choice]

        # Додаємо покупку до бази даних
        db.insert({
            'user_id': user_id,
            'product': product_choice,
            'price': selected['price'],
            'timestamp': timestamp
        })

        await update.callback_query.message.reply_text(
            f"Ви успішно придбали {selected['name']} за {selected['price']}!"
        )
    else:
        await update.callback_query.answer('Невідомий товар')
