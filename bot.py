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

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)




def getSeatsAmount():
    
    # Go to the webpage 
    req = requests.get('http://wwwapps.ehabitat.net/rvrcdh/')
    req.raise_for_status()


    # Get capacity
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    pic = soup.select('body > div > div:nth-child(1) > div > div > h1')
    textToRegex = pic[0].text.strip()

    
    piclinkRegex = re.compile(r'(\d)+ / (\d)+')
    mo = piclinkRegex.search(textToRegex)
    return mo.group()

    


def checkSeats(update, context):
    capacity = getSeatsAmount()
    context.bot.send_message(chat_id=update.effective_chat.id, text = "{} seats taken".format(capacity))


def checkFucksGiven(update, context):
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo='https://i.pinimg.com/originals/3f/8e/c9/3f8ec91740507ec9d82a2acee1e1635a.jpg')



def start(update, context):
    name = update.message.from_user.first_name;
    context.bot.send_message(chat_id=update.effective_chat.id, text = """
Hello {}!
/checkseats
""".format(name))





def main():
    updater = Updater(token = '1855391169:AAGuzaD2E6AA_mDPXRIuhT5IPv9JZ3ERlFU', use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('checkseats', checkSeats))

    dispatcher.add_handler(CommandHandler('checkfucksgiven', checkFucksGiven))
    
    updater.start_polling()

    updater.idle()
    



if __name__ == '__main__':
    main()
    



