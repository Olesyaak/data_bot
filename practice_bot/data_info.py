import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate
from dotenv import load_dotenv


load_dotenv()


def get_info(worksheet):
    values = worksheet.get_all_values()
    table = tabulate(values, headers="firstrow", tablefmt="simple")
    return table


def get_info_no_head(worksheet):
    values = worksheet.get_all_values()
    table = tabulate(values, tablefmt="simple")
    return table


def start_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    keyboard = [
        [InlineKeyboardButton("Зарплата Junior DS", callback_data='junior')],
        [InlineKeyboardButton("Зарплата midle DS", callback_data='midle')],
        [InlineKeyboardButton("Зарплата SE DS", callback_data='se')],
        [InlineKeyboardButton("Топ 3 высокооплачиваемых направления", callback_data='top_3')],
        [InlineKeyboardButton("Профессии data_science_analytics", callback_data='dsa')],
        [InlineKeyboardButton("Профессии machine_Learning", callback_data='ml')],
        [InlineKeyboardButton("Профессии specialized_roles", callback_data='sr')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=chat.id,
                             text='{} Нажми на кнопку, которая тебя интересует'.format(name),
                             reply_markup=reply_markup)


def button_click(update, context):
    query = update.callback_query
    data = query.data
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "bot-project-420418-c1520370e9dc.json", scope
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open("bot")
    if data == "junior":
        worksheet = spreadsheet.worksheet("EN")
        query.message.reply_text("Данные для junior: \n" + '\n' + get_info(worksheet))
    elif data == "midle":
        worksheet = spreadsheet.worksheet("MI")
        query.message.reply_text("Данные для midle: \n" + '\n' + get_info(worksheet))
    elif data == "se":
        worksheet = spreadsheet.worksheet("SE")
        query.message.reply_text("Данные для senior: \n" + '\n' + get_info(worksheet))
    elif data == "top_3":
        worksheet = spreadsheet.worksheet("top3")
        values = worksheet.get_all_values()
        alignments = ['c', 'r'] * len(values[0])
        table = tabulate(values, headers="firstrow", tablefmt="simple", stralign=alignments)
        query.message.reply_text("Данные: \n" + '\n' + table)
    elif data == "dsa":
        worksheet = spreadsheet.worksheet("DSA")
        query.message.reply_text("Профессии группы data_science_analytics: \n" + '\n' + get_info_no_head(worksheet))
    elif data == "ml":
        worksheet = spreadsheet.worksheet("ML")
        query.message.reply_text("Профессии группы machine_Learning: \n" + '\n' + get_info_no_head(worksheet))
    elif data == 'sr':
        worksheet = spreadsheet.worksheet("SR")
        query.message.reply_text("Профессии группы specialized_roles: \n" + '\n' + get_info_no_head(worksheet))


def get_message(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text='Извини, но я могу предоставить только информацию, указанную выше. '
                                  'Поэтому нажми кнопочку. '
                                  'Но, если честно, то я бы советовал тебе изучить одну из профессий из '
                                  'списков топ-3, переехать в Швейцарию и устроиться в компанию среднего уровня')


def main():
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_up))
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    dispatcher.add_handler(MessageHandler(Filters.text, get_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
