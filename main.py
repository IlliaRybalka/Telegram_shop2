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
        descriprion = "Telegram Premium: Отримайте доступ до ексклюзивних функцій, таких як завантаження файлів великого розміру, додаткові реакції на повідомлення, а також можливість використовувати спеціальні аватари."
        await query.edit_message_text(text=f"Ви вибрали Telegram Premium. Ціна: $4.99\n\n{descriprion}")
    elif choice == 'discord_nitro':
        descriprion = "Discord Nitro: Насолоджуйтесь покращеним досвідом спілкування з функціями, такими як використання анімованих емодзі, завантаження більших файлів, та можливість використовувати різні ніки на різних серверах."
        await query.edit_message_text(text=f"Ви вибрали Discord Nitro. Ціна: $9.99\n\n{descriprion}")
    elif choice == 'game_cheats':
        descriprion = "Чіти на ігри: Отримайте ексклюзивні чіти для ваших улюблених ігор, що допоможуть вам досягти нових рівнів і відкрити приховані можливості."
        await query.edit_message_text(text=f"Ви вибрали Чіти на ігри. Ціна: $19.99\n\n{descriprion}")

    keyboard = [
        [InlineKeyboardButton("Отримати товар", url='https://www.donationalerts.com/r/yazva1810')]
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