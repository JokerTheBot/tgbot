import html
from typing import Optional, List
from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown, mention_html
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot import dispatcher, SUDO_USERS, OWNER_USERNAME, OWNER_ID
import tg_bot.modules.sql.gpromote_sql as sql

sudo_list = sql.get_sudo_list()
for i in sudo_list:
   SUDO_USERS.append(i)

def add_to_sudo(user_id, bot):
    try:
        user_chat = bot.get_chat(user_id)
    except BadRequest as excp:
        message.reply_text(excp.message)
        return
    sql.gpromote_user(user_id, user_chat.username or user_chat.first_name)
    SUDO_USERS.append(user_id)


@run_async
def gpromote(bot: Bot, update: Update):
    args = List[str]
    message = update.effective_message
    banner = update.effective_user
    user_id = extract_user(message, args)
    if banner.id == OWNER_ID:
        if not user_id:
            message.reply_text("You don't seems to be referring to a user.")
            return
        elif int(user_id) in SUDO_USERS:
            message.reply_text("The user is already a sudo user.")
            return
        elif int(user_id) == OWNER_ID:
            message.reply_text("The specified user is my owner! No need add him to SUDO_USERS list!")
            return
        else:
            add_to_sudo(user_id, bot)
            message.reply_text("Succefully added to SUDO user list!!")
            return
    else:
        message.reply_text("Only owner of the bot, {} can do this".format(OWNER_USERNAME))
        return

@run_async
def ungpromote(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_chat = bot.get_chat(user_id)
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text("No user refered")
        return
    if user_chat.type != 'private':
        message.reply_text("That's not a user!")
        return
    if not sql.is_user_sudo(user_id):
        message.reply_text("{} is not a sudo user".format(user_chat.username))
        return
    sql.ungpromote_user(user_id)
    message.reply_text("User no longer have SUDO user rights!")



GPROMOTE_HANDLER = CommandHandler("gpromote", gpromote, filters = CustomFilters.sudo_filter)
UNGPROMOTE_HANDLER = CommandHandler("ungpromote", ungpromote, filters=Filters.user(OWNER_ID)
dispatcher.add_handler(GPROMOTE_HANDLER)
dispatcher.add_handler(UNGPROMOTE_HANDLER)
