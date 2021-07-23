import bs4, sys, requests, os, logging, re
from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
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





# /start command
def start(update, context):
    name = update.message.from_user.first_name;
    context.bot.send_message(chat_id=update.effective_chat.id, text = """
Hello {}!
This bot allows you to eat with your fwiends UwU
/startsession in a group to start FoodSanta-ing.
""".format(name))


sessionMessageID = 0

def startSession(update, context):
    chatID = update.effective_chat.id
    if chatID > 0:
        # User sent this message
        context.bot.send_message(chatID, text = "This command should be used in a group")

    elif sessionExists(chatID) == False:      
        # Add session to list of sessions
        addSession(chatID)

        reply_keyboard = [[InlineKeyboardButton("Join", callback_data="Join")]]
        reply_markup=InlineKeyboardMarkup(reply_keyboard)
        context.bot.sendMessage(chatID, 'Hey yall, click join to participate in this session. Once everydone is done, you may /closesession', reply_markup = reply_markup)

    else:
        # Session already exists in group
        context.bot.send_message(chatID, text = """
dude wtf a session alr exists.""")
        

def closeSession(update, context) -> None:
    chatID = update.effective_chat.id
    users = getSession(chatID).userList
    textString = "Session closed\nThose in the session:\n"
    for user in users.values:
        textString = textString + user.name + '\n'
    context.bot.send_message(chatID, text = textString)


    # Randomise assignments


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user = query.from_user
    choice = query.data
    
    # Add user to current session
    if choice == 'Join':
        # Get chat ID
        chatID = update.effective_chat.id

        # Add user to Session
        session = getSession(update.effective_chat.id)

        if (session.addUser(user)):
            context.bot.sendMessage(chatID, '{} joined the session!'.format(user.username))
        else:
            context.bot.sendMessage(chatID, '{} is already in the session!'.format(user.username))

        




def main():
    updater = Updater(token = '1855391169:AAGuzaD2E6AA_mDPXRIuhT5IPv9JZ3ERlFU', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('startsession', startSession))

    dispatcher.add_handler(CommandHandler('closesession', closeSession))

    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()
    



if __name__ == '__main__':
    main()
    



