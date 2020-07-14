from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, ChosenInlineResultHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async

import keyboards
import private
import strings
import db

@run_async
def inline_query_handler(update, context):
    """
    Menu to be shown in inline, when @BotName is typed
    """
    query = update.inline_query.query
    if not query: query = strings.DEFAULT_QUEUE_NAME 
    results = [
        InlineQueryResultArticle(
            id=1,
            title=strings.REALTIME_QUERY_TITLE,
            description=strings.REALTIME_QUERY_DESC,
            thumb_url=strings.REALTIME_QUERY_IMG,
            input_message_content=InputTextMessageContent(
                db.Queue.print_hello(query_name=query),
                parse_mode=ParseMode.MARKDOWN),
            reply_markup=keyboards.INIT
            )
        ]
    update.inline_query.answer(results)

@run_async
def inline_option_handler(update, context):
    """
    Create new db schema on inline option click
    """
    chosen = update.chosen_inline_result
    new_queue = db.Queue(
        queue_id=chosen.inline_message_id,
        author_id=chosen.from_user.id,
        title=chosen.query if chosen.query else strings.DEFAULT_QUEUE_NAME)
    new_queue.save()




"""Inline button callbacks"""
"""Initial state"""
@run_async
@db.Queue.check_author(err_msg=strings.ALERT_NOTAUTHOR_START)
def start(update, context):
    query = update.callback_query
    query.answer()
    markup = keyboards.MAIN
    if db.Queue.is_prioritized(query.inline_message_id):
        markup = keyboards.MAIN_PRIORITIZED
    query.edit_message_text(
        db.Queue.print_queue(query.inline_message_id),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN)

@run_async
@db.Queue.check_author(err_msg=strings.ALERT_NOTAUTHOR_CONFIG)
def enter_config_type(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        db.Queue.print_config(query.inline_message_id),
        reply_markup=keyboards.CONFIG,
        parse_mode=ParseMode.MARKDOWN)




"""Config state"""
@run_async
@db.Queue.check_author(err_msg=strings.ALERT_NOTAUTHOR_CONFIG)
def config_back(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        db.Queue.print_hello(queue_id=query.inline_message_id),
        reply_markup=keyboards.INIT,
        parse_mode=ParseMode.MARKDOWN)

@run_async
@db.Queue.check_author(err_msg=strings.ALERT_NOTAUTHOR_CONFIG)
def config_sort(update, context):
    query = update.callback_query
    query.answer()
    db.Queue.toggle_sortby(query.inline_message_id)
    query.edit_message_text(
        db.Queue.print_config(query.inline_message_id),
        reply_markup=keyboards.CONFIG,
        parse_mode=ParseMode.MARKDOWN)

@run_async
@db.Queue.check_author(err_msg=strings.ALERT_NOTAUTHOR_CONFIG)
def config_reverse(update, context):
    query = update.callback_query
    query.answer()
    db.Queue.toggle_reverse(query.inline_message_id)
    query.edit_message_text(
        db.Queue.print_config(query.inline_message_id),
        reply_markup=keyboards.CONFIG,
        parse_mode=ParseMode.MARKDOWN)

@run_async
@db.Queue.check_author(err_msg=strings.ALERT_NOTAUTHOR_CONFIG)
def config_priority(update, context):
    query = update.callback_query
    query.answer()
    db.Queue.toggle_priority(query.inline_message_id)
    query.edit_message_text(
        db.Queue.print_config(query.inline_message_id),
        reply_markup=keyboards.CONFIG,
        parse_mode=ParseMode.MARKDOWN)




"""Running state"""
@run_async
@db.Queue.check_queue(err_msg=strings.ALREADY_IN_QUEUE_MSG)
def add(update, context):
    query = update.callback_query
    query.answer()
    priority = 0
    if query.data == keyboards.MAIN_ADD_TOP_ID:
        priority = -1
    elif query.data == keyboards.MAIN_ADD_BOTTOM_ID:
        priority = 1
    markup = keyboards.MAIN
    if db.Queue.is_prioritized(query.inline_message_id):
        markup = keyboards.MAIN_PRIORITIZED
    user = db.User(
        user_id=update.effective_user.id,
        username=update.effective_user.username,
        fullname=f"{update.effective_user.first_name}{' '+update.effective_user.last_name if update.effective_user.last_name else ''}",
        priority=priority)
    db.Queue.objects(queue_id=query.inline_message_id).update_one(push__queue=user)
    query.edit_message_text(
        db.Queue.print_queue(query.inline_message_id),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN)

@run_async
@db.Queue.check_queue(to_remove=True)
def delete(update, context):
    query = update.callback_query
    query.answer()
    markup = keyboards.MAIN
    if db.Queue.is_prioritized(query.inline_message_id):
        markup = keyboards.MAIN_PRIORITIZED
    db.Queue.objects(queue_id=query.inline_message_id).update_one(pull__queue__user_id=update.effective_user.id)
    query.edit_message_text(
        db.Queue.print_queue(query.inline_message_id),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN)






def main():

    updater = Updater(private.telegram_token, use_context=True)

    dp = updater.dispatcher

    #Inline handlers
    dp.add_handler(InlineQueryHandler(inline_query_handler))
    dp.add_handler(ChosenInlineResultHandler(inline_option_handler))

    #Initial-state button handlers
    dp.add_handler(CallbackQueryHandler(start, pattern=f"^{keyboards.INIT_START_ID}$"))
    dp.add_handler(CallbackQueryHandler(enter_config_type, pattern=f"^{keyboards.INIT_CONFIG_ID}$"))

    #Config-state button handlers
    dp.add_handler(CallbackQueryHandler(config_back, pattern=f"^{keyboards.CONFIG_BACK_ID}$"))
    dp.add_handler(CallbackQueryHandler(config_sort, pattern=f"^{keyboards.CONFIG_SORT_ID}$"))
    dp.add_handler(CallbackQueryHandler(config_reverse, pattern=f"^{keyboards.CONFIG_REVERSE_ID}$"))
    dp.add_handler(CallbackQueryHandler(config_priority, pattern=f"^{keyboards.CONFIG_PRIORITY_ID}$"))

    #Running-state button handlers
    dp.add_handler(CallbackQueryHandler(add, pattern=f"^{keyboards.MAIN_ADD_ID}$"))
    dp.add_handler(CallbackQueryHandler(add, pattern=f"^{keyboards.MAIN_ADD_TOP_ID}$"))
    dp.add_handler(CallbackQueryHandler(add, pattern=f"^{keyboards.MAIN_ADD_BOTTOM_ID}$"))
    dp.add_handler(CallbackQueryHandler(delete, pattern=f"^{keyboards.MAIN_DELETE_ID}$"))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()