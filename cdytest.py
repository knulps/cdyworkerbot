import requests
import json

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules

TOKEN = 'YOUR TOKEN'

URL_CDY_LIVE_STATS = "http://pool.cdy.one/api/live_stats"
URL_CDY_WORKER_STATS = "http://pool.cdy.one/api/worker_stats?{}"

addr_dict = {}

# bot = telegram.Bot(token = TOKEN)

# try:
#     updates = bot.getUpdates()
#     chat_id = updates[-1].message.chat.id

#     if len(updates) > 0:
#         print(updates[-1].message)
#         if updates[-1].message.text == "/start":
#             bot.sendMessage(chat_id = chat_id, text="I'm cdypool bot, type /addr \'yourWorkerAddress\'")
# except Exception as e:
#     print('error occured {}'.format(e))

# message reply function


def get_message(bot, update):
    print(update.message)
    # update.message.reply_text("got text")
    # update.message.reply_text(update.message.text)


def start_command(bot, update):
    print(update.message.text)
    update.message.reply_text(
        "I'm cdypool bot, type /addr \'yourWorkerAddress\'")

def addr_command(bot,update):
    print(update.message.text)
    try:
        if '/addr ' in update.message.text:
            address = update.message.text.replace('/addr ','')
            if str(update.message.chat.id) in addr_dict:
                print("before value : ", addr_dict[str(update.message.chat.id)])
            addr_dict[str(update.message.chat.id)] = address
            update.message.reply_text("your worker address is updated to {}".format(address))
            print("updated value : ", addr_dict[str(update.message.chat.id)])
        else :
            update.message.reply_text("Wrong command, type /addr \'yourWorkerAddress\'")
    except Exception as e:
        print('error occured {}'.format(e))

def worker_info_command(bot,update):
    print(update.message.text)
    print("info , dict : ", addr_dict)
    try:
        if str(update.message.chat.id) not in addr_dict or addr_dict[str(update.message.chat.id)] is None:
            print(1)
            update.message.reply_text("please add your worker address with /addr \'yourWorkerAddress\'")
        else:
            print(2)
            print("addr_dict[update.message.chat.id] is not None, search {}".format(addr_dict[str(update.message.chat.id)]))
            res = requests.get(URL_CDY_WORKER_STATS.format(addr_dict[str(update.message.chat.id)]), timeout=100)
            if res.status_code == 200:
                json_result = json.loads(res.text)
                # print("json_result :", json_result)
                print(json_result['workers'].keys())
                str_result = ""
                worker_list = list(json_result['workers'].keys())
                for index, worker in enumerate(worker_list):
                    str_result = str_result + str(index) + ". worker : " + worker +", hashrate(now) : " + json_result['workers'][worker]['hashrateString']
                    if index != len(worker_list) -1:
                        str_result = str_result + "\n"
                update.message.reply_text(str_result)
            else:
                print("get request failed") 
    except Exception as e:
        print('error occured {}'.format(e))

updater = Updater(TOKEN)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

start_handler = CommandHandler('start', start_command)
updater.dispatcher.add_handler(start_handler)

addr_handler = CommandHandler('addr',addr_command)
updater.dispatcher.add_handler(addr_handler)

worker_info_handler = CommandHandler('info', worker_info_command)
updater.dispatcher.add_handler(worker_info_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()

# res = requests.get(URL_CDY_WORKER_STATS, timeout=100)
# if res.status_code == 200:
#     json_result = json.loads(res.text)
#     print(json_result.miner, json_result.workers)
# else:
#     print("get request failed")


# def setWorker(addr_):
#     addr = addr_

# #


# def getWorkerUrl():
#     if addr is None:
#         return None
#     else:
#         return URL_CDY_WORKER_STATS.format(addr)
