from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Функція для обробки стартової команди
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привіт! Надішліть мені емодзі, і я поверну його код.')

# Функція для обробки емодзі (як тексту)
async def emoji_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    # Перевіряємо, чи є в повідомленні емодзі (емодзі - це символи Unicode)
    if text:
        emoji_codes = ' '.join(f'U+{ord(char):04X}' for char in text)
        await update.message.reply_text(f'Коди емодзі: {emoji_codes}')

def main() -> None:
    # Введіть свій токен бота тут
    token = '7399033739:AAFLuTWC_dgslWXR75ZY48UCAIr9qKY9gZk'

    # Створення аплікації
    application = Application.builder().token(token).build()

    # Реєстрація обробників команд та повідомлень
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, emoji_handler))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()

