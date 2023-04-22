from checking_dates import reminder


async def print_dates(context):
    for i in reminder(context.job.user_id):
        await context.bot.send_message(chat_id=context.job.chat_id, text=i)