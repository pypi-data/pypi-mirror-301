import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.api.remote.sb_user import get_user_limits
from src.api.remote.sb_history import get_analysis_history
from src.api.reports import handle_get_reports_by_uuid
from src.api.security import check_user_and_api_key, check_user_groups
from src.db.users import db_get_user
from src.lang.director import humanize
import os
from src.api.remote.sb_task_info import process_task_info, ResultType


async def check_user_access(bot, user_id: int):
    logging.debug(f"Checking access for user {user_id}")
    user = await db_get_user(user_id)
    if not user:
        logging.warning(f"User {user_id} not found")
        return False, humanize("USER_NOT_FOUND")
    if user[4]:
        logging.warning(f"User {user_id} is banned")
        return False, humanize("USER_BANNED")
    if user[5]:
        logging.warning(f"User {user_id} is deleted")
        return False, humanize("USER_DELETED")
    
    api_key, error_message = await check_user_and_api_key(user_id)
    if error_message:
        logging.warning(f"API key error for user {user_id}: {error_message}")
        return False, error_message
    
    logging.debug(f"API Key for user {user_id} (first 5 chars): {api_key[:5]}...")
    
    required_group_ids = os.getenv('REQUIRED_GROUP_IDS', '')
    if not await check_user_groups(bot, user_id, required_group_ids):
        logging.warning(f"User {user_id} not in required groups")
        return False, humanize("NOT_IN_REQUIRED_GROUPS")
    
    return True, api_key

async def sandbox_api_action(update: Update, context: ContextTypes.DEFAULT_TYPE, action_func):
    user_id = update.effective_user.id
    logging.debug(f"User ID: {user_id} requesting sandbox API action: {action_func.__name__}")

    access_granted, result = await check_user_access(context.bot, user_id)
    if not access_granted:
        await update.callback_query.answer(text=result)
        logging.warning(f"Access denied for user {user_id}: {result}")
        return

    logging.debug(f"Access granted for user {user_id}, executing {action_func.__name__}")
    await action_func(update, context, result)

async def get_report_by_uuid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sandbox_api_action(update, context, _get_report)

async def get_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sandbox_api_action(update, context, _show_history)

async def _get_report(update: Update, context: ContextTypes.DEFAULT_TYPE, api_key: str):
    logging.debug(f"Getting report for user {update.effective_user.id} with API key (first 5 chars): {api_key[:5]}")
    context.user_data['api_key'] = api_key
    await handle_get_reports_by_uuid(update, context)

async def _show_history(update: Update, context: ContextTypes.DEFAULT_TYPE, api_key: str):
    user_id = update.effective_user.id
    logging.debug(f"User ID: {user_id} requesting history.")
    logging.debug(f"API Key (first 5 chars): {api_key[:5]}...")

    limit = 10
    skip = 0
    logging.debug(f"Fetching analysis history with params: limit={limit}, skip={skip}")
    history = await get_analysis_history(api_key, limit, skip)

    if isinstance(history, dict) and "error" in history:
        await update.callback_query.answer(text=history["error"])
        logging.error(f"Error fetching history: {history['error']}")
        return

    if not isinstance(history, list):
        logging.error(f"Expected history to be a list, but got {type(history)}.")
        await update.callback_query.answer(text=humanize("INVALID_DATA_FORMAT"))
        return

    if not history:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=humanize("NO_ANALYSIS_HISTORY"))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=humanize("LAST_TEN_REPORTS"))
        
        for analysis in history:
            verdict = analysis.get('verdict', 'Unknown')
            date = analysis.get('date', '')
            name = analysis.get('name', '')
            uuid = analysis.get('uuid', '')
            tags = analysis.get('tags', [])

            text_message = process_task_info(verdict, date, name, uuid, tags, ResultType.TEXT)

            if text_message.strip():
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text_message, parse_mode='MarkdownV2')

    keyboard = [
        [InlineKeyboardButton(humanize("MENU_BUTTON_BACK"), callback_data='sandbox_api')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=humanize("CHOOSE_OPTION"), reply_markup=reply_markup)

async def show_api_limits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await sandbox_api_action(update, context, _show_api_limits)

async def _show_api_limits(update: Update, context: ContextTypes.DEFAULT_TYPE, api_key: str):
    user_id = update.effective_user.id
    api_key, error_message = await check_user_and_api_key(user_id)

    if error_message:
        await update.callback_query.answer(text=error_message)
        return
    limits_message = await get_user_limits(api_key)

    if isinstance(limits_message, dict) and "error" in limits_message:
        await update.callback_query.answer(text=limits_message["error"])
        return
    await update.callback_query.edit_message_text(limits_message)

    keyboard = [
        [InlineKeyboardButton(humanize("MENU_BUTTON_BACK"), callback_data='sandbox_api')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(humanize("CHOOSE_OPTION"), reply_markup=reply_markup)
