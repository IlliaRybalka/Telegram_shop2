import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from constants import TOKEN
from handlers.start_handler import start
from handlers.history_handler import view_history
from handlers.button_handler import button_handler
from handlers.message_handler import message_handler

def main() -> None:
    # Налаштування логування
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    application = Application.builder().token(TOKEN).build()

    # Обробники команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('history', view_history))

    # Обробник callback-запитів
    application.add_handler(CallbackQueryHandler(button_handler))

    # Обробник текстових повідомлень
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()