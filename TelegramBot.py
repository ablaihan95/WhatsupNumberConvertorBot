import logging

from selenium.webdriver.chrome import webdriver
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from Selenium import parser

# from Parser import parser

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    received_message = update.message.text
    message_to_answer = "не смог обработать"
    count = 0
    if not received_message.__contains__("http"):
        message_to_answer = converter(received_message)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_to_answer)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Придется подождать 2-3 минуты...")
        tns: str = parser(received_message)
        for tn in tns:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=converter(tn))


def converter(text):
    if text.startswith("8"):
        text = '7' + text[1:]
    new_string = text.replace(" ", "").replace("(", "").replace(")", "").replace("+", "").replace("-", "")
    return "https://wa.me/" + new_string


if __name__ == '__main__':
    application = ApplicationBuilder().token('token').build()

start_handler = CommandHandler('start', start)

echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

application.add_handler(start_handler)
application.add_handler(echo_handler)

application.run_polling()
