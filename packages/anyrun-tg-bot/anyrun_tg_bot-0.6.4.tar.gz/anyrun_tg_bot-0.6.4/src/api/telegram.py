import logging
import asyncio
from telegram import Update, User
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest, TelegramError, NetworkError
from src.lang.context import set_user_language_getter, set_language_for_user
from src.lang.director import humanize
from src.api.security import setup_telegram_security, check_in_groups
from src.api.menu import show_main_menu, create_main_menu
from src.db.users import db_add_user
from importlib.metadata import version

def get_user_language(user: User) -> str:
    return user.language_code if user.language_code else 'en'

set_user_language_getter(get_user_language)

async def setup_telegram_bot(config):
    TOKEN = config.get('TELEGRAM_TOKEN')
    logging.debug(f"Setting up Telegram bot with token: {TOKEN[:5]}...{TOKEN[-5:]}.")
    
    try:
        TOKEN = setup_telegram_security(TOKEN)
        
        logging.debug('Building Telegram application')
        application = Application.builder().token(TOKEN).build()
        logging.debug('Telegram application built successfully')
        
        required_group_ids = config.get('REQUIRED_GROUP_IDS')
        logging.debug(f'Required group IDs: {required_group_ids}')

        await application.initialize()
        await application.bot.initialize()
        
        bot_in_groups = await check_in_groups(application.bot, application.bot.id, is_bot=True, required_group_ids=required_group_ids)
        
        # Проверяем, что бот состоит во всех требуемых группах
        if not all(info[0] for info in bot_in_groups.values()):
            logging.warning(f'Bot is not in all required groups. Missing groups: {list(bot_in_groups.keys())[:200]}')
        else:
            logging.debug('Bot is in all required groups.')
        
        logging.debug('Adding command handlers')
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", show_main_menu))
        
        from src.api.handlers import setup_handlers
        setup_handlers(application)
        
        application.add_error_handler(handle_telegram_error)
        
        logging.debug('Command handlers added successfully')
        return application
    except Exception as e:
        logging.exception(f'Error during Telegram bot setup: {e}')
        raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.debug(f'User started the bot: user_id={update.effective_user.id}')
    set_language_for_user(update.effective_user)
    
    try:
        await db_add_user(update.effective_user.id)
    except Exception as e:
        logging.error(f"Error adding/updating user in database: {e}")
    
    welcome_message = humanize("WELCOME_MESSAGE").format(version=version("anyrun-tg-bot"))
    await update.message.reply_text(welcome_message)
    await show_main_menu(update, context)

async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_language_for_user(update.effective_user)

async def handle_telegram_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    if isinstance(error, NetworkError):
        logging.error(f"NetworkError: {error}. Retrying connection...")
        await retry_connection(context)
    elif isinstance(error, BadRequest):
        if "Query is too old" in str(error):
            await update.effective_message.reply_text(humanize("QUERY_EXPIRED"))
            await show_main_menu(update, context)
        else:
            logging.error(f"BadRequest error: {error}")
    elif isinstance(error, TelegramError):
        logging.error(f"TelegramError: {error}")
    else:
        logging.error(f"Unexpected error: {error}")
        await update.effective_message.reply_text(humanize("ERROR_OCCURRED"))

async def retry_connection(context: ContextTypes.DEFAULT_TYPE, delay: int = 60):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            await context.bot.get_me()
            logging.info("Reconnected to Telegram successfully.")
            return
        except NetworkError as e:
            wait_time = delay * (2 ** attempt)
            logging.warning(f"Retrying in {wait_time} seconds due to NetworkError: {e}")
            await asyncio.sleep(wait_time)
    logging.critical("Failed to reconnect to Telegram after multiple attempts.")
