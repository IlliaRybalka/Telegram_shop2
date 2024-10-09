from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from tinydb import TinyDB, Query

# Ініціалізація бази даних для зберігання історії покупок
db = TinyDB('purchases.json')
UserQuery = Query()

TOKEN = '7399033739:AAFLuTWC_dgslWXR75ZY48UCAIr9qKY9gZk'

# Функція для старту з клавіатурою
async def start(update: Update, context: CallbackContext) -> None:
    # Кнопки для основних команд
    keyboard = [
        [KeyboardButton("/start"), KeyboardButton("Історія покупок")],
        [KeyboardButton("Показати ціни"), KeyboardButton("Меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        'Виберіть опцію або скористайтеся командами з клавіатури:', 
        reply_markup=reply_markup
    )

# Функція для показу цін
async def show_prices(update: Update, context: CallbackContext) -> None:
    options = [
        ("Telegram Premium 💎 - $4.99", 'telegram_premium'),
        ("Discord Nitro ⚡️ - $9.99", 'discord_nitro'),
        ("Чіти на ігри 🎮 - $19.99", 'game_cheats')
    ]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Оберіть продукт з ціною:', reply_markup=reply_markup)

# Функція для обробки натискання кнопок продуктів
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    choices = {
        'telegram_premium': {
            'description': "Telegram Premium: Отримайте доступ до ексклюзивних функцій...",
            'price': "$4.99"
        },
        'discord_nitro': {
            'description': "Discord Nitro: Насолоджуйтесь покращеним досвідом...",
            'price': "$9.99"
        },
        'game_cheats': {
            'description': "Чіти на ігри: Отримайте ексклюзивні чіти для ваших улюблених ігор...",
            'price': "$19.99"
        }
    }

    choice = query.data
    if choice in choices:
        selected = choices[choice]

        # Збереження інформації про покупку в базу даних
        user_id = update.callback_query.from_user.id
        db.insert({'user_id': user_id, 'product': choice, 'price': selected['price']})

        await query.edit_message_text(
            text=f"Ви вибрали {choice.replace('_', ' ').title()}. Ціна: {selected['price']}\n\n{selected['description']}",
            parse_mode='Markdown'
        )

        # Додаємо кнопки для повернення в меню та оформлення замовлення
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='back')],
            [InlineKeyboardButton("Меню", callback_data='back_to_menu')],
            [InlineKeyboardButton("Оформить заказ", callback_data='place_order', url='https://t.me/illya_bot')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)

# Функція для перегляду історії покупок
async def view_history(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    purchases = db.search(UserQuery.user_id == user_id)

    if not purchases:
        await update.message.reply_text("Ваша історія покупок порожня.")
        return

    history_text = "Ваша історія покупок:\n"
    keyboard = []

    for purchase in purchases:
        product_name = purchase['product'].replace('_', ' ').title()
        history_text += f"- {product_name} ({purchase['price']})\n"
        keyboard.append([InlineKeyboardButton(f"Повторити замовлення {product_name}", callback_data=purchase['product'])])

    # Додаємо кнопку для повернення до меню
    keyboard.append([InlineKeyboardButton("Меню", callback_data='back_to_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(history_text, reply_markup=reply_markup)

# Функція для обробки натискання команд або кнопок
async def button_handler(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    
    if message_text == "Історія покупок":
        await view_history(update, context)
    elif message_text == "Показати ціни":
        await show_prices(update, context)
    elif message_text == "Меню":
        await start(update, context)
    else:
        await update.message.reply_text('Будь ласка, оберіть опцію з меню або скористайтеся кнопками.')

# Основна функція
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Обробники для команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('history', view_history))

    # Обробник для натискання кнопок на клавіатурі
    application.add_handler(CallbackQueryHandler(button))

    # Обробник для текстових команд
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
