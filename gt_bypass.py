import logging
from telegram.ext import Updater, CommandHandler
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the conversion function
def convert_url(update, context):
    url = update.message.text.split()[-1]  # Extract URL from the message
    token = re.search(r'token=([^&]+)', url).group(1)  # Extract token from the URL
    converted_url = f"https://gtlinks.me/{token}"  # Construct the converted URL
    update.message.reply_text(converted_url)  # Reply with the converted URL

def main():
    # Set up the Telegram Bot
    updater = Updater("6667741068:AAHCnUPRXcUbU6rkpzAZylUUm8FDlXyXGiw", use_context=True)
    dp = updater.dispatcher

    # Define a command handler for the /convert command
    dp.add_handler(CommandHandler("convert", convert_url))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started polling...")

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()