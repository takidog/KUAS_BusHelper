#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram.ext import  CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging

import Login
import Sqlite_func
import time,datetime
import re

import telegramcalendar
import Config
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

Account_keyboard = [['輸入NKUST帳號'],
                  ['離開']]
                
Password_keyboard = [['輸入NKUST密碼'],
                  ['離開']]

exit_keyboard = [['離開']]

order_keyboard = [['查詢已預約車次'],
                  ['查詢車次','預約乘車'],
                  ['取消預約'],
                  ['離開']]

start_keyboard = [['/start']]

Acc_markup = ReplyKeyboardMarkup(Account_keyboard, one_time_keyboard=True)
Pas_markup = ReplyKeyboardMarkup(Password_keyboard, one_time_keyboard=True)
exit_markup = ReplyKeyboardMarkup(exit_keyboard, one_time_keyboard=True)
order_markup = ReplyKeyboardMarkup(order_keyboard, one_time_keyboard=True)
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)


rm_keyboard = ReplyKeyboardRemove()

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def reg_check(chat_id):
    return Sqlite_func.chatID_check(chat_id)

def start(bot, update):
    try:
        update.message.reply_text("""hi! 你好~\n這邊採取自動登入的方式，所以會有保存學校帳號密碼的問題\n有能力的話建議自行架設!\n我自己也很怕保管這些QQ""",reply_markup=rm_keyboard)
        user_chat_id = update['message']['chat']['id']
        
        if reg_check(user_chat_id) == True:
            update.message.reply_text("hi! 已註冊~\n約車約起來!!!!",reply_markup=order_markup)
        else:
            update.message.reply_text("尚未註冊QQ",reply_markup=Acc_markup)
    except:
        update.message.reply_text("ohh... not good QQ, have some error\nplz try again!")
        return ConversationHandler.END
    
    #update.message.reply_text("yee",reply_markup=markup)
    
    #print(update['message']['chat']['id'])

    return CHOOSING


def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    if text == "輸入NKUST帳號":
        update.message.reply_text("單純學號而已哦\n請輸入: ",reply_markup=rm_keyboard)
    elif text == "輸入NKUST密碼":
        update.message.reply_text("(如果怕有隱私問題，輸入完再刪除那則回應哦)\n請輸入: ",reply_markup=rm_keyboard)
    elif text == "預約乘車":
        update.message.reply_text("請輸入查詢後的BusID哦",reply_markup=rm_keyboard)
    elif text == "取消預約":
        bus = Login.Core()
        Acc,Pass = Sqlite_func.getNKUST_Acc(update['message']['chat']['id'])
        if bus.Login_check(Acc,Pass) == True:
            res = bus.get_reserve_bus()
            tx = ''
            for i in res:
                c = '燕巢>>建工'
                if i['carryType'] == 'A':
                    c = '建工>>燕巢'

                text = "cancel_ID:%s 時間: %s方向:%s\n"%(i['cancelKey'],time.strftime('%m-%d %H:%M',time.strptime(i['time'],"%Y-%m-%d %H:%M")),c)
                tx += text
        update.message.reply_text(tx)
        update.message.reply_text("請輸入要取消的cancel_ID哦",reply_markup=rm_keyboard)

    elif text == "離開":
        user_data.clear()
        update.message.reply_text('Bye~',reply_markup=start_markup)
        return ConversationHandler.END
    elif text == "查詢已預約車次":
        bus = Login.Core()
        Acc,Pass = Sqlite_func.getNKUST_Acc(update['message']['chat']['id'])
        if bus.Login_check(Acc,Pass) == True:
            res = bus.get_reserve_bus()
            for i in res:
                c = '燕巢>>建工'
                if i['carryType'] == 'A':
                    c = '建工>>燕巢'

                text = "時間: %s方向:%s"%(time.strftime('%m-%d %H:%M',time.strptime(i['time'],"%Y-%m-%d %H:%M")),c)
                update.message.reply_text(text,reply_markup=order_markup)
        return TYPING_CHOICE
    
    elif text == "查詢車次":
        if reg_check(update['message']['chat']['id']) == True:
            update.message.reply_text("選擇一個日期吧!\n(14日內))")
            update.message.reply_text("查詢中..",reply_markup=telegramcalendar.create_calendar())
            return TYPING_CHOICE
        else:
            update.message.reply_text("oh.. 查詢車次之前需要先註冊登入哦!",reply_markup=start_markup)
            return TYPING_CHOICE
    return TYPING_REPLY


def custom_choice(bot, update):
    update.message.reply_text('')

    return TYPING_CHOICE

def inline_handler(bot,update): # for calender use 
    selected,date = telegramcalendar.process_calendar_selection(bot, update)
    if selected:
        y,m,d=date.year,date.month,date.day
        diff =  datetime.date(y,m,d) - datetime.date.today()
        #print(diff.days)
        if diff.days > 14 or diff.days < 0:
            bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="超出可查詢的範圍QQ",
                        reply_markup=order_markup)
        else:
            bus = Login.Core()
            Acc,Pwd = Sqlite_func.getNKUST_Acc(str(update['callback_query']['message']['chat']['id']))
            if bus.Login_check(Acc,Pwd) == True:
                res = bus.search(y,m,d)
                #print(res)
                bot.send_message(chat_id=update.callback_query.from_user.id,
                        text=res,
                        reply_markup=order_markup)

def received_information(bot, update, user_data): # here save data
    text = update.message.text
    try:
        category = user_data['choice']
        user_data[category] = text
        del user_data['choice']
    except:
        done(bot,update,user_data,end=1)
    #print(user_data)
    #print(update['message']['chat']['id'])
    if user_data.get('預約乘車') != None:
        if re.match(r'^(\d{5,})$', text) != None:
            #print(text)
            bus = Login.Core()
            Acc,Pwd = Sqlite_func.getNKUST_Acc(update['message']['chat']['id'])
            bus.Login_check(Acc,Pwd)
            res = bus.book(text)
            update.message.reply_text(res,reply_markup=order_markup)
            user_data.clear()
        return CHOOSING
    if user_data.get('取消預約') != None:
        if re.match(r'^(\d{7,})$', text) != None:
            #print(text)
            bus = Login.Core()
            Acc,Pwd = Sqlite_func.getNKUST_Acc(update['message']['chat']['id'])
            bus.Login_check(Acc,Pwd)
            res = bus.unbook(text)
            update.message.reply_text(res,reply_markup=order_markup)
            user_data.clear()
        return CHOOSING

    if user_data.get('輸入NKUST帳號') != None and user_data.get('輸入NKUST密碼') == None:
        update.message.reply_text("----",reply_markup=Pas_markup) 
        return CHOOSING
    elif user_data.get('輸入NKUST帳號') != None and user_data.get('輸入NKUST密碼') != None:
        update.message.reply_text("準備登入測試><")
        # SQL injection
        if re.match(r'^([A-Za-z0-9]\w{3,13})$',user_data.get('輸入NKUST密碼')) == None or re.match(r'^(\d{6,13})$',user_data.get('輸入NKUST帳號')) == None:
            update.message.reply_text("輸入的東西好像怪怪的哦，全!部!重!來!\n /start 重來吧!")
            user_data.clear()
            return ConversationHandler.END                                                                           
        #here Login Check 
        bus = Login.Core()
        res = bus.Login_check(user_data.get('輸入NKUST帳號'),user_data.get('輸入NKUST密碼'))
        #
        if res == True:
            update.message.reply_text("NKUST登入成功，已經將你的Telegtam跟NKUST帳號連結了\n請從 /start 重來吧!")
            #save data to Sqlite
            Sqlite_func.sql_execute("INSERT INTO NKUST (Account,Password,Telegram_chatID) ","'%s','%s','%s'"%(user_data.get('輸入NKUST帳號'),user_data.get('輸入NKUST密碼'),update['message']['chat']['id']))
            user_data.clear()
            return ConversationHandler.END
        if res == False:
            update.message.reply_text("NKUST登入失敗，不是伺服器掛了就是帳號密碼錯誤\n請從 /start 重來吧!")
            user_data.clear()
            return ConversationHandler.END

    return CHOOSING

def done(bot, update, user_data,end=0):
    try:
        if 'choice' in user_data:
            del user_data['choice']
    except:
        return ConversationHandler.END
    if end == 0:
        update.message.reply_text('Bye~',reply_markup=start_markup)

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    conf = Config.config()
    updater = Updater(conf.get('Telegram','api'))
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(查詢已預約車次|查詢車次)$',
                                    regular_choice,
                                    pass_user_data=True),
                       RegexHandler('^(輸入NKUST帳號|輸入NKUST密碼|完成)$',
                                    regular_choice,
                                    pass_user_data=True),
                       RegexHandler('^(取消預約|預約乘車)$',
                                    regular_choice,
                                    pass_user_data=True),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^(Done|離開)$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CallbackQueryHandler(inline_handler))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    Sqlite_func.sql_check()
    main()
