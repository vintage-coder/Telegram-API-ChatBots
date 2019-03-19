import handlers
import logging
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler,CallbackQueryHandler)

CLAIM,VEHICLE,LICENCE,CONTACT,OTP,LOCATION,PICTURE=range(7)



updater = Updater(token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
dispatcher = updater.dispatcher

#===========================================================Handlers===========================


conversation_handler=ConversationHandler(
                                        entry_points=[CommandHandler('start',handlers.start)],

                                        states={

                                            CLAIM:[CallbackQueryHandler(handlers.claim)],

                                            VEHICLE :[CallbackQueryHandler(handlers.vehicle)],

                                            LICENCE : [MessageHandler(Filters.text,handlers.licence,pass_user_data=True)],

                                            CONTACT : [MessageHandler(Filters.contact,handlers.contact,pass_user_data=True)],

                                            OTP: [MessageHandler(Filters.text,handlers.otp,pass_user_data=True)],

                                            LOCATION :[MessageHandler(Filters.location,handlers.location,pass_user_data=True)],

                                            PICTURE : [MessageHandler(Filters.photo,handlers.picture,pass_user_data=True)],

                                            },
                                        fallbacks=[CommandHandler('cancel',handlers.cancel)]
                                        )




#===========================================Dispatchers========================================


dispatcher.add_handler(conversation_handler)

#=====================================================Signals================================
updater.start_polling()
updater.idle()
