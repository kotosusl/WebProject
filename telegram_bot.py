import logging
from telegram.ext import Application
from TOKEN import TOKEN
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from data import db_session
from load_olimpycs_db import new_olimpycs
from load_subjects import load_subjects

from start import start
from help import help
from adding import adding
from stop import stop
from add_response import add_response
from unset_response import unset_response
from button import button
from unsetting import unsetting
from unsetting_all import unsetting_all
from yes_or_no import yes_or_no
from finding import finding
from sort_type import sort_type
from finding_response import finding_response


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main():
    db_session.global_init("db/relations.db")
    load_subjects()
    new_olimpycs()
    application = Application.builder().token(TOKEN).build()
    conv_handler_add = ConversationHandler(entry_points=[CommandHandler('add', adding)],
                                           states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_response)]},
                                           fallbacks=[CommandHandler('stop', stop)])

    conv_handler_unset = ConversationHandler(entry_points=[CommandHandler('unset', unsetting)],
                                             states={
                                                 1: [MessageHandler(filters.TEXT & ~filters.COMMAND, unset_response)]},
                                             fallbacks=[CommandHandler('stop', stop)])

    conv_handler_unset_all = ConversationHandler(entry_points=[CommandHandler('unset_all', unsetting_all)],
                                                 states={1: [CallbackQueryHandler(yes_or_no)]},
                                                 fallbacks=[CommandHandler('stop', stop)])

    conv_handler_find = ConversationHandler(entry_points=[CommandHandler('find', finding)],
                                            states={1: [CallbackQueryHandler(sort_type)],
                                                    2: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                                       finding_response)]},
                                            fallbacks=[CommandHandler('stop', stop)])

    application.add_handler(conv_handler_find)
    application.add_handler(conv_handler_unset_all)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(conv_handler_add)
    application.add_handler(conv_handler_unset)
    application.run_polling()


if __name__ == '__main__':
    main()