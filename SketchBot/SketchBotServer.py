import telegram
import handlers
from telegram.ext import Updater,Filters
from telegram.ext import CommandHandler,MessageHandler,ConversationHandler


updater = Updater(token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
dispatcher = updater.dispatcher

TYPE_TEXT,UPLOAD_PHOTO=range(2)

#================================Handlers======================================================================

conv_handler=ConversationHandler(
                entry_points=[CommandHandler('start',handlers.start)],
                states={
                    TYPE_TEXT:[MessageHandler(Filters.text,handlers.put_text,pass_user_data=True)],
                    UPLOAD_PHOTO:[MessageHandler(Filters.photo,handlers.process_photo,pass_user_data=True)],
                },
                fallbacks=[CommandHandler('done',handlers.done,pass_user_data=True)]
)

#================================Dispatchers ==================================
dispatcher.add_handler(conv_handler)
dispatcher.add_error_handler(handlers.error)

updater.start_polling()
updater.idle()
