import logging
from telegram.ext import Application
from TOKEN import TOKEN
from datetime import datetime
from telegram.ext import CommandHandler
from data import db_session


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def start(update, context):
    db_session.global_init("db/blogs.db")
    await update.message.reply_html(f"""Приветствую, {update.effective_user.first_name}.
                                        \n """)


def main():
    db_session.global_init("db/relations.db")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()