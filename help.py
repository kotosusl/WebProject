async def help(update, context):
    await update.message.reply_html(f"""Этот бот умеет:

/start - запустить бот;
/find - найти олимпиады по фильтрам;
/add - быстрое добавление олимпиады в напоминания;
/stop - прервать процесс;
/unset - удалить напоминание;
/unset_all - удалить все напоминания.""")
