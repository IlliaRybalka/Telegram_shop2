from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = '7399033739:AAFLuTWC_dgslWXR75ZY48UCAIr9qKY9gZk'

async def start(update: Update, context: CallbackContext) -> None:
    options = [
        ("Telegram Premium", 'telegram_premium'),
        ("Discord Nitro", 'discord_nitro'),
        ("Чіти на ігри", 'game_cheats')
    ]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Виберіть опцію:', reply_markup=reply_markup)

async def show_prices(update: Update, context: CallbackContext) -> None:
    options = [
        ("Telegram Premium - $4.99", 'telegram_premium'),
        ("Discord Nitro - $9.99", 'discord_nitro'),
        ("Чіти на ігри - $19.99", 'game_cheats')
    ]
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text('Оберіть продукт з ціною:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        await show_prices(update, context)
        return

    choices = {
        'telegram_premium': {
            'description': "Telegram Premium: Отримайте доступ до ексклюзивних функцій, таких як завантаження файлів великого розміру, додаткові реакції на повідомлення, а також можливість використовувати спеціальні аватари.",
            'price': "$4.99",
            'image_url': "https://th.bing.com/th/id/OIP.0ekVtvo0UbK6yjwOZZZSUAHaEt?w=280&h=180&c=7&r=0&o=5&pid=1.7",
            'payment_url': "https://illyarybalka08.wixsite.com/-site"
        },
        'discord_nitro': {
            'description': "Discord Nitro: Насолоджуйтесь покращеним досвідом спілкування з функціями, такими як використання анімованих емодзі, завантаження більших файлів, та можливість використовувати різні ніки на різних серверах.",
            'price': "$9.99",
            'image_url': "https://example.com/discord_nitro_image.jpg",
            'payment_url': "https://illyarybalka08.wixsite.com/-site"
        },
        'game_cheats': {
            'description': "Чіти на ігри: Отримайте ексклюзивні чіти для ваших улюблених ігор, що допоможуть вам досягти нових рівнів і відкрити приховані можливості.",
            'price': "$19.99",
            'image_url': "https://example.com/game_cheats_image.jpg",
            'payment_url': "https://illyarybalka08.wixsite.com/-site"
        }
    }

    choice = query.data
    if choice in choices:
        selected = choices[choice]
        await query.edit_message_text(
            text=f"Ви вибрали {choice.replace('_', ' ').title()}. Ціна: {selected['price']}\n\n{selected['description']}\n\n[Зображення]({selected['image_url']})",
            parse_mode='Markdown'
        )

    keyboard = [
        [InlineKeyboardButton("Отримати товар", url=selected['payment_url'])],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()