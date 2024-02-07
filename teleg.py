bot_token = '6281201453:AAHy5KAq4BBbjXFMzjYYAINgDUpA6Nok1TY'


from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler

def start_handler(update: Update, context: CallbackContext):
    # Your start handler logic
    pass

def text_handler(update: Update, context: CallbackContext):
    message = update.message
    text = message.text

    # Process the received text or perform any desired actions
    # For example, you can print the received message
    print(f"Received message: {text}")

    # Perform your desired actions with the text here
    # ...

def main():
    # Your main function code

    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_handler))
    dp.add_handler(MessageHandler(None, text_handler))  # None acts as a placeholder for the filter function
    updater.start_polling()
    updater.idle()
    # Rest of your main function code

if __name__ == '__main__':
    main()