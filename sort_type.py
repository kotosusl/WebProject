from telegram import ReplyKeyboardMarkup


async def sort_type(update, context):
    query = update.callback_query
    status = query.data
    context.user_data['status'] = status
    reply_markup = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_markup)
    if status == 'class*0':
        await context.bot.send_message(text='Введите класс для поиска', chat_id=update.effective_chat.id,
                                       reply_markup=markup)
        return 2
    if status == 'subject*0':
        await context.bot.send_message(text='Введите предмет для поиска', chat_id=update.effective_chat.id,
                                       reply_markup=markup)
        return 2
    if status == 'name*0':
        await context.bot.send_message(text='Введите название олимпиады для поиска', chat_id=update.effective_chat.id,
                                       reply_markup=markup)
        return 2
