from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from tinydb import TinyDB, Query
from datetime import datetime
import json

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
    if query:
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

            # Відображення інформації про товар з кнопкою "Купити"
            await query.edit_message_text(
                text=f"Ви вибрали {choice.replace('_', ' ').title()}. Ціна: {selected['price']}\n\n{selected['description']}",
                parse_mode='Markdown'
            )

            # Додаємо кнопку "Купити"
            keyboard = [
                [InlineKeyboardButton("Купити", callback_data=f'buy_{choice}')],
                [InlineKeyboardButton("Назад", callback_data='back')],
                [InlineKeyboardButton("Меню", callback_data='back_to_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_reply_markup(reply_markup=reply_markup)

# Функція для обробки покупки
async def handle_purchase(update: Update, context: CallbackContext, product_choice: str) -> None:
    user_id = update.callback_query.from_user.id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Пошук продукту у виборах
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

        # Use TinyDB to add purchase to the database
        db.insert({
            'user_id': user_id,
            'product': product_choice,
            'price': selected['price'],
            'timestamp': timestamp
        })

        await update.callback_query.message.reply_text(
            f"Ви успішно придбали {product_choice.replace('_', ' ').title()} за {selected['price']}!"
        )

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
        history_text += f"- {product_name} ({purchase['price']}) - {purchase.get('timestamp', 'Немає часу')}\n"
        keyboard.append([InlineKeyboardButton(f"Повторити замовлення {product_name}", callback_data=purchase['product'])])

    # Додаємо кнопку для повернення до меню
    keyboard.append([InlineKeyboardButton("Меню", callback_data='back_to_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(history_text, reply_markup=reply_markup)

# Функція для обробки натискання команд або кнопок
async def button_handler(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        query = update.callback_query
        if query.data:  # Check if data exists
            message_text = query.data

            if message_text.startswith('buy_'):
                product_choice = message_text[4:]
                await handle_purchase(update, context, product_choice)
            elif message_text == 'back':
                await show_prices(update, context)
            elif message_text == 'back_to_menu':
                await start(update, context)
            else:
                # Викликаємо функцію button для обробки вибору товару
                await button(update, context)
        else:
            await update.callback_query.answer('Помилка: Дані відсутні')
    elif update.message:
        message_text = update.message.text
        if message_text == "Історія покупок":
            await view_history(update, context)
        elif message_text == "Показати ціни":
            await show_prices(update, context)
        elif message_text == "Меню":
            await start(update, context)
        else:
            await update.message.reply_text('Будь ласка, оберіть опцію з меню або скористайтеся кнопками.')
    else:
        # Handle unexpected update types
        print("Отримано неочікуваний тип оновлення")

# Основна функція
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Обробники для команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('history', view_history))

    # Обробник для натискання кнопок на клавіатурі
    application.add_handler(CallbackQueryHandler(button_handler))

    # Обробник для текстових команд
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
