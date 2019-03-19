import Message
from telegram import ChatAction,InlineKeyboardButton,InlineKeyboardMarkup
import telegram
from telegram.ext import Filters,ConversationHandler
from twilio.rest import Client
import random


account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
client = Client(account_sid, auth_token)

CLAIM,VEHICLE,LICENCE,CONTACT,OTP,LOCATION,PICTURE=range(7)

def start(bot, update):

    bot.sendChatAction(update.message.chat_id, action=ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text=Message.CLAIM,parse_mode='html')
    reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("Check New Model",callback_data="New Model")],
                                                    [telegram.InlineKeyboardButton("Reasses my Insurance",callback_data="Reasses")],
                                                    [telegram.InlineKeyboardButton("File a Claim",callback_data="claim")]])

    bot.sendPhoto(chat_id=update.message.chat_id, caption="<b>Choose Any one?</b>",photo=open("insurance_claim.jpg","rb"),
                reply_markup=reply_markup,parse_mode="html")

    return CLAIM

def claim(bot,update):
    query=update.callback_query

    if query.data=='New Model':

        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,show_alert=True,text="You clicked new model.There is no New model processing further!")


    elif query.data=='Reasses':
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,show_alert=True,text="You clicked Reasses Insurance,There is no further activity")

    elif query.data=="claim":

        reply_markup = telegram.InlineKeyboardMarkup([[telegram.InlineKeyboardButton("Vehicle",callback_data="vehicle")],
                                                        [telegram.InlineKeyboardButton("Personal Accident",callback_data="accident")],
                                                        [telegram.InlineKeyboardButton("Other",callback_data="other")]])

        bot.sendPhoto(chat_id=update.callback_query.message.chat.id,photo=open("car_insurance.jpg","rb"),\
                    caption="<b>Choose the one below?</b>", reply_markup=reply_markup,parse_mode="html")

        return VEHICLE


def vehicle(bot,update):
    query=update.callback_query

    if query.data=='vehicle':
        bot.sendMessage(chat_id=update.callback_query.message.chat_id,text=Message.LICENCE,parse_mode='html')
        return LICENCE

    elif query.data=='accident':
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,text="currently not updated accident")
    elif query.data=='other':
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id,text="currently not updated other")


def licence(bot,update,user_data):
    user_data['licence']=update.message.text
    print('The licence number is:',update.message.text)
    contact_keyboard = telegram.KeyboardButton(text="Send Contact", request_contact=True)
    custom_keyboard = [[ contact_keyboard ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,one_time_keyboard=True)

    bot.sendMessage(chat_id=update.message.chat_id,text=Message.CONTACT,\
                    parse_mode="html",reply_markup=reply_markup)
    return CONTACT

def contact(bot,update,user_data):
    user_data['phone_number']=update.message.contact
    print('The Contact Number is:',user_data['phone_number'])
    phone_number="+"+update.message.contact.phone_number
    First_name=update.message.from_user.first_name
    Last_name=update.message.from_user.last_name
    print('The first name %s and Last name %s:'%(First_name,Last_name))
    print('The phone is:',phone_number)
    otp=random.randint(100000,1000000)
    body=("Hey , %s %s. The Mobile verification has been sent to your registered mobile number %s\
            .The OTP is %s"%(First_name,Last_name,phone_number,str(otp)))

    message = client.messages \
                            .create(
                                    body=body,
                                    from_='+17012899320',
                                    to=phone_number
                                    )
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.OTP,\
                    parse_mode="html")
    return OTP



def otp(bot,update,user_data):
    user_data['otp']=update.message.text
    print('The Entered OTP is:',update.message.text)

    bot.sendMessage(chat_id=update.message.chat_id,text=Message.LOCATION,parse_mode="html")
    location_keyboard = telegram.KeyboardButton(text="Send Location", request_location=True)
    custom_keyboard = [[ location_keyboard ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,one_time_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id,text="Share your location with me?",reply_markup=reply_markup,one_time_keyboard=True)

    return LOCATION


def location(bot,update,user_data):
    user_data['location']=update.message.location
    print('The location is :',user_data['location'])
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.PICTURE,parse_mode="html")


    return PICTURE

def picture(bot,update,user_data):
    user_data['picture']=update.message.photo[-1]
    user_data['link']=update.message.photo[-1].file_id
    print('The Sent photo is:',user_data['picture'])
    photo_file=bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    print('The link of photo in server is:',user_data['link'])
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.INFORM,parse_mode="html")
    return ConversationHandler.END


def cancel(bot,update):
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.END,parse_mode='html')
