from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = '7399033739:AAFLuTWC_dgslWXR75ZY48UCAIr9qKY9gZk'

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Telegram Premium", callback_data='telegram_premium')],
        [InlineKeyboardButton("Discord Nitro", callback_data='discord_nitro')],
        [InlineKeyboardButton("Чіти на ігри", callback_data='game_cheats')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Виберіть опцію:', reply_markup=reply_markup)

async def show_prices(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Telegram Premium - $4.99", callback_data='telegram_premium')],
        [InlineKeyboardButton("Discord Nitro - $9.99", callback_data='discord_nitro')],
        [InlineKeyboardButton("Чіти на ігри - $19.99", callback_data='game_cheats')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text('Оберіть продукт з ціною:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    choice = query.data

    if choice == 'telegram_premium':
        await query.edit_message_text(text="Ви вибрали Telegram Premium. Ціна: $4.99")
    elif choice == 'discord_nitro':
        await query.edit_message_text(text="Ви вибрали Discord Nitro. Ціна: $9.99")
    elif choice == 'game_cheats':
        await query.edit_message_text(text="Ви вибрали Чіти на ігри. Ціна: $19.99")

    await show_prices(update, context)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
