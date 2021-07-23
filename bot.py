import bs4, sys, requests, os, logging, re
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Session class
from Session import Session

# Abstraction of session dictionary
from db import (
    sessionExists,
    addSession,
    getSession,
)


#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


# Dictionary of all sessions


def startSession(update, context):
    chatID = update.effective_chat.id;
    if chatID > 0:
        # User sent this message
        context.bot.send_message(chatID, text = "This command should be used in a group")

    elif sessionExists(chatID) == False:
        context.bot.send_message(chatID, text = """
Hey yall, click join to participate in this session.""")

        addSession(chatID)
        # Group sent this message
    
    elif sessionExists(chatID) == True:
        context.bot.send_message(chatID, text = """
Dude wtf the session already exists""")

    else:
        context.bot.send_message(chatID, text = """
you shouldnt reach here""")


        




def start(update, context):
    name = update.message.from_user.first_name;
    context.bot.send_message(chat_id=update.effective_chat.id, text = """
Hello {}!
This bot allows you to eat with your fwiends UwU
""".format(name))





def main():
    updater = Updater(token = '1855391169:AAGuzaD2E6AA_mDPXRIuhT5IPv9JZ3ERlFU', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('startsession', startSession))
    
    updater.start_polling()

    updater.idle()
    



if __name__ == '__main__':
    main()
    



