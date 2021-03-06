import bs4, sys, requests, os, logging, re
from dotenv import load_dotenv
import os, logging
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    PollHandler,
)

# Session class
from Session import Session

# Abstraction of session dictionary
from db import (
    sessionExists,
    addSession,
    getSession,
    getSessions,
    deleteSession
)

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


# use env file
load_dotenv()

# /start command
def start(update, context):
    name = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text = """
Hello {}!
This bot allows you to eat with your fwiends UwU
/startsession in a group to start FoodSanta-ing.
For the bot to work, private message the bot /start.
""".format(name))


sessionMessage = 0

def startSession(update, context):
    global sessionMessage
    
    chatID = update.effective_chat.id
    if chatID > 0:
        # User sent this message
        context.bot.send_message(chatID, text = "This command should be used in a group")

    elif sessionExists(chatID) == False:      
        # Add session to list of sessions
        addSession(chatID)

        reply_keyboard = [
            [InlineKeyboardButton("Join", callback_data="Join")], 
            [InlineKeyboardButton("Leave", callback_data="Leave")],
            [InlineKeyboardButton("Start", callback_data="Start")]
            ]
        reply_markup=InlineKeyboardMarkup(reply_keyboard)
        sessionMessage = context.bot.sendMessage(chatID, 'Hey yall, a FOOD SANTA 🎅 session has been created! Click join to participate in this session. For the bot to work, private message the bot /start.', reply_markup = reply_markup)

    else:
        # Session already exists in group
        context.bot.send_message(chatID, text = """
 A session alr exists in this chat.""")
        

def closeSession(update, context) -> None:
    global sessionMessage

    # Generate message
    chatID = update.effective_chat.id

    # Delete and reset session
    context.bot.delete_message(chat_id=chatID, message_id=sessionMessage.message_id)
    sessionMessage = 0
    if (deleteSession(chatID)):
        context.bot.send_message(chatID, text = "Session closed. /startsession again to restart")
    else:
        context.bot.send_message(chatID, text = "There's no session to delete bruh")



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

        if session.status:
            context.bot.sendMessage(chatID, 'Session has already started')
        elif (session.addUser(user)):
            context.bot.sendMessage(chatID, '{} joined the session!'.format(user.username))
        else:
            context.bot.sendMessage(chatID, '{} is already in the session!'.format(user.username))
    # Remove user from current session
    elif choice == 'Leave':
                 # Get chat ID
        chatID = update.effective_chat.id

        # Add user to Session
        session = getSession(update.effective_chat.id)
        if session.status:
            context.bot.sendMessage(chatID, 'Session has already started')
        if (session.removeUser(user)):
            context.bot.sendMessage(chatID, '{} has left the session!'.format(user.username))
        else:
            context.bot.sendMessage(chatID, '{} is not even in the session bro.'.format(user.username))
    # Start the current session once everyone is ready
    elif choice == 'Start':
        # Get chat ID
        chatID = update.effective_chat.id
        session = getSession(update.effective_chat.id)

        if len(session.userList) < 2:
            context.bot.sendMessage(chatID, 'There are not enough participants to start a session :(')
        elif session.startSession():
            context.bot.sendMessage(chatID, 'Session started! Check your DMs! Meanwhile...')
            setPriceRange(update, context)
        else:
            context.bot.sendMessage(chatID, 'Session already started. Check your DMs.')



def setPriceRange(update, context):
    options = ['<$5','$5 - $10','$10 - $15', '$15 - $20', '>$20']
    chatID = update.effective_chat.id
    message = context.bot.send_poll(chatID, "Let's standardise a price range!", options, is_anonymous=False)

    # Save some info about the poll the bot_data for later use in receivePollAnswer
    payload = {
        message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
    }

    context.bot_data.update(payload)



def receivePollAnswer(update: Update, context: CallbackContext) -> None:
    poll_id = update.poll.id

    # the bot can receive closed poll updates we don't care about
    if update.poll.is_closed:
        return

    chatID = context.bot_data[poll_id]['chat_id']
    if update.poll.total_voter_count == len(getSession(chatID).userList):
        try:
            quiz_data = context.bot_data[update.poll.id]
            

            # Get array of PollOption objects
            optionArray = update.poll.options
            highestVote = 0
            highestPrice = ""
            for option in optionArray:
                if option.voter_count > highestVote:
                    highestPrice = option.text
                    highestVote = option.voter_count
            getSession(chatID).priceRange = highestPrice

            context.bot.sendMessage(chatID, 'As per the votes, your recommended price range is {}. Check your DMs'.format(highestPrice))

        # poll answer update is from an old poll
        except KeyError:
            return
        context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])


def getDetail(update, context):

    chatID = update.effective_chat.id
    if not chatID > 0:
        # User sent this message in a group
        context.bot.send_message(chatID, text = "This command should be used in private message")
    else:
        sess = None
        address = update.message.text.split(" ")
        address2 = address[1:]
        address3 = ''
        for i in address2:
            address3 += i + " "
        currentUser = update.effective_user.id
        allsess = getSessions()
        for sess in allsess:
            if currentUser in getSession(sess).userList.keys():
                getSession(sess).userList[currentUser].setAddress(str(address3))
                break

        if (sess == None):
            return

        finished = True
        for user in getSession(sess).userList.values():
            if user.address == "":
                finished = False
            else:
                finished = finished & True

        update.message.reply_text("You've sent " + address3 + ". Please wait for the rest to complete their entry!")
        if finished == True:
            for user in getSession(sess).userList.values():
                Session.messageUser(getSession(sess), user.userId, "Hello! you'll be sending your goods to "+ user.assigned.username + ", here are the details: " + user.assigned.address + ". Have Fun!!!!")
            deleteSession(sess)

# def test(update, context):
#     chatID = update.effective_chat.id
#     getSession(chatID).startAssignment()


def main():
    updater = Updater(token = os.getenv('TOKEN'), use_context = True)
    PORT = int(os.environ.get('PORT', 80))
    updater = Updater(token = os.getenv('TOKEN'), use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('startsession', startSession))

    dispatcher.add_handler(CommandHandler('closesession', closeSession))

    dispatcher.add_handler(CallbackQueryHandler(button))

    # dispatcher.add_handler(CommandHandler('randomassign', test))

    dispatcher.add_handler(CommandHandler('details', getDetail))

    dispatcher.add_handler(PollHandler(receivePollAnswer))

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=os.getenv('TOKEN'))
    updater.bot.setWebhook('https://food-santa.herokuapp.com/' + os.getenv('TOKEN'))

    updater.idle()


if __name__ == '__main__':
    main()
    



