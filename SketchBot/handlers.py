import Message
import cv2
import logging
TYPE_TEXT,UPLOAD_PHOTO=range(2)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO,filename='imagebot.log')
logger=logging.getLogger(__name__)


def start(bot,update):
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.IMAGE,parse_mode='html')
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.TEXT,parse_mode='markdown')
    logger.info('Start handler was initiated.....')
    return TYPE_TEXT

def process_photo(bot,update,user_data):
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    font = cv2.FONT_HERSHEY_SIMPLEX
    image=cv2.imread(photo_file.download('user_photo.jpg'),1)
    logger.info('The uploaded image was downloaded...........')
    cv2.putText(image,user_data['name'],(100,100), font, 3,(0,0,255),5)
    logger.info('The Text was written on the image...........')
    cv2.imwrite('user_photo.jpg',image)
    photo = open('user_photo.jpg', 'rb')
    bot.send_photo(chat_id=update.message.chat_id, photo=photo)
    logger.info('The modified image was sent back to telegram client......')
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.DONE,parse_mode='markdown')
    return ConversationHandler.END

def put_text(bot,update,user_data):
    user_data['name']=update.message.text
    logger.info('The text was got from the telegram client............')
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.PHOTO,parse_mode='markdown')
    return UPLOAD_PHOTO

def done(bot,update):
    bot.sendMessage(chat_id=update.message.chat_id,text=Message.DONE,parse_mode='markdown')
    logger.info('The telegram fallback function was called..............')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
