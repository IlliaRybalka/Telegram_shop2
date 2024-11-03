import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from constants import TOKEN
from handlers.start_handler import start
from handlers.history_handler import view_history
from handlers.button_handler import button_handler
from handlers.message_handler import message_handler

# Error handler
def error_handler(update, context):
    logging.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('history', view_history))

    # Callback query handler
    application.add_handler(CallbackQueryHandler(button_handler))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
