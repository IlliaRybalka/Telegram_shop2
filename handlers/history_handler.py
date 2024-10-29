from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import db, UserQuery
from constants import PRODUCT_CHOICES

async def view_history(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    purchases = db.search(UserQuery.user_id == user_id)

    if not purchases:
        await update.message.reply_text("Ваша історія покупок порожня.")
        return

    history_text = "Ваша історія покупок:\n"
    keyboard = []

    for purchase in purchases:
        product_info = PRODUCT_CHOICES.get(purchase['product'], {})
        product_name = product_info.get('name', purchase['product'].replace('_', ' ').title())
        history_text += f"- {product_name} ({purchase['price']}) - {purchase.get('timestamp', 'Немає часу')}\n"
        keyboard.append([InlineKeyboardButton(f"Повторити замовлення {product_name}", callback_data=purchase['product'])])

    keyboard.append([InlineKeyboardButton("Меню", callback_data='back_to_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(history_text, reply_markup=reply_markup)
