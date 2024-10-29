from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from tinydb import TinyDB, Query
from datetime import datetime

# Ініціалізація бази даних
db = TinyDB('purchases.json')
UserQuery = Query()

# Функція старту
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

# Функція показу цін
async def show_prices(update: Update, context: CallbackContext) -> None:
    options = [
        ("Telegram Premium 💎 - $4.99", 'telegram_premium'),
        ("Discord Nitro ⚡️ - $9.99", 'discord_nitro'),
        ("Чіти на ігри 🎮 - $19.99", 'game_cheats')
    ]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Оберіть продукт з ціною:', reply_markup=reply_markup)

# Функція для обробки вибору продукту
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

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

    if data in choices:
        selected = choices[data]
        await query.edit_message_text(
            text=f"Ви вибрали {data.replace('_', ' ').title()}. Ціна: {selected['price']}\n\n{selected['description']}"
        )

        keyboard = [
            [InlineKeyboardButton("Купити", callback_data=f'buy_{data}')],
            [InlineKeyboardButton("Назад", callback_data='back')],
            [InlineKeyboardButton("Меню", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)
    else:
        await query.answer('Невідома команда')

# Функція для обробки покупки
async def handle_purchase(update: Update, context: CallbackContext, product_choice: str) -> None:
    user_id = update.callback_query.from_user.id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

    if product_choice in choices:
        selected = choices[product_choice]

        # Додаємо покупку до бази даних
        db.insert({
            'user_id': user_id,
            'product': product_choice,
            'price': selected['price'],
            'timestamp': timestamp
        })

        await update.callback_query.message.reply_text(
            f"Ви успішно придбали {product_choice.replace('_', ' ').title()} за {selected['price']}!"
        )
    else:
        await update.callback_query.answer('Невідомий товар')

# Функція перегляду історії покупок
async def view_history(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    purchases = db.search(UserQuery.user_id == user_id)

    if not purchases:
        await update.message.reply_text("Ваша історія покупок порожня.")
        return

    history_text = "Ваша історія покупок:\n"
    keyboard = []

    for purchase in purchases:
        product_name = purchase['product'].replace('_', ' ').title()
        history_text += f"- {product_name} ({purchase['price']}) - {purchase.get('timestamp', 'Немає часу')}\n"
        keyboard.append([InlineKeyboardButton(f"Повторити замовлення {product_name}", callback_data=purchase['product'])])

    keyboard.append([InlineKeyboardButton("Меню", callback_data='back_to_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(history_text, reply_markup=reply_markup)

# Функція обробки текстових повідомлень (кнопки клавіатури)
async def message_handler(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    if message_text == "Історія покупок":
        await view_history(update, context)
    elif message_text == "Показати ціни":
        await show_prices(update, context)
    elif message_text == "Меню":
        await start(update, context)
    else:
        await update.message.reply_text('Будь ласка, оберіть опцію з меню або скористайтеся кнопками.')

# Функція обробки callback-запитів (кнопки InlineKeyboard)
async def callback_query_handler(update: Update, context: CallbackContext) -> None:
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
    else:
        # Обробка вибору продукту
        await button(update, context)
