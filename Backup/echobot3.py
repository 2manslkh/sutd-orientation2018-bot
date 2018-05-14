#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import read_write_to_firebase as pb
import logging
import string
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Get Admin/Execs List
admins = pb.pb_read("Admins")
admins = list(admins.values())
execs = pb.pb_read("Execs")
execs = list(execs.values())
execs.extend(admins)
OG_IDS_D = pb.pb_read("OG_IDS")
print(OG_IDS_D)
OG_IDS = list(OG_IDS_D.values())
print("Admins: {}".format(admins))
print("Execs: {}".format(execs))
print("OGS: {}".format(OG_IDS))

# Telegram bot Auth Key
AuthKey = "566390966:AAEPvfBKfUhb1eSct9Ty1lseKHPfzHgfQWQ"

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

# =============================================================================
# HOUSEKEEPING COMMANDS begin the command with _
# =============================================================================

def _checkadmin(update, level):
    """ Check if command sender has enough priviliege """
    security = {2:admins,1:execs}
    user = update.message.chat.id
    print(user)
    if user not in security[level]:
        update.message.reply_text("You do not have enough privilege!")
        return False

def _button(bot, update):
    callback = {'1':'DOORS OPEN',
                '2':'DOORS CLOSED',
                '3':'other'}
    query = update.callback_query
    query_num = query.data
    
    def open_doors(bot, update):
        for _id in OG_IDS:
            print(_id)
            bot.send_message(chat_id=_id,
                             text="⚠️ DOORS ARE NOW OPEN! ⚠️")
            
    def close_doors(bot,update):
        for _id in OG_IDS:
            bot.send_message(chat_id=_id,
                             text="⚠️ WARNING! DOORS ARE NOW CLOSED! ⚠️")
    
    if query_num == '1':
        open_doors(bot, update)
    elif query_num == '2':
        close_doors(bot, update)
    
    bot.edit_message_text(text="Selected option: {}".format(callback[query_num]),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def _error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    
# =============================================================================
# REGISTRATION
# =============================================================================

def adminaccess(bot, update, args):
    """ User Input: /adminaccess <password>"""
    """ args[0] = <password> """
    """ Adds user to admin/execs whitelist """
    
    if len(args) != 1:
        update.message.reply_text('Request admin by the following format:\n/adminaccess <password>')
    else:
        user_id = update.message.from_user.id
        if args[0] == "adminme9090":
            pb.pb_write(user_id,user_id,"Admins")
            update.message.reply_text("You are granted Level 2 Access")
        elif args[0] == "adminme0905":
            pb.pb_write(user_id,user_id,"Execs")
            update.message.reply_text("You are granted Level 1 Access")
        else:
            update.message.reply_text("Invalid Password!")

def registerog(bot, update, args):
    """ User Input: /adminaccess <password>"""
    """ args[0] = <password> """
    """ Adds user to admin whitelist """
    OG_IDS = int(args[0])
    if len(args) != 1:
        update.message.reply_text('Register your OG telegram group using the following format:\n/registerog <OG #>')
    else:
        if OG_IDS not in list(range(1,25)):
            update.message.reply_text("Please enter a OG Number from 1-24!")
            return
        if str(OG_IDS) in list(pb.pb_read("OG_IDS").keys()):
            update.message.reply_text("Sorry, that OG is already registered!")
            return
        
        # Gets the group ID
        user_id = update.message.chat.id
        
        # Adds the group ID to the list of OGL GROUP ID in pyrebase
        pb.pb_write(OG_IDS, user_id, "OG_IDS")
        
        # Feedback message
        update.message.reply_text("OG Registered!")
        
# =============================================================================
# LEVEL 2 (ADMIN) COMMANDS
# =============================================================================

def refreshdata(bot, update):
    """ Refresh the data in the bot """
    if _checkadmin(update,2) == False:
        return
    
    admins = pb.pb_read("Admins")
    admins = list(admins.values())
    execs = pb.pb_read("Execs")
    execs = list(execs.values())
    execs.extend(admins)
    OG_IDS = list(pb.pb_read("OG_IDS").values())
    update.message.reply_text("ADMINS:\n{}\n\nEXECS:\n{}\n\nOG IDS:\n{}".format(admins,execs,OG_IDS))
    

def configuredoors(bot, update):
    """ Sends the Door status message to all OGS """
    
    if _checkadmin(update,2) == False:
        return
    
    keyboard = [[InlineKeyboardButton("OPEN DOORS", callback_data='1'),
                 InlineKeyboardButton("CLOSE DOORS", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

# =============================================================================
# LEVEL 1 (EXECS) COMMANDS
# =============================================================================
def addpoints(bot, update, args):
    """ User Input: /addpoints <OG> <Points> """
    """ args[0] = <OG> args[1] = <Points> """
    """ Updates points in firebase """
    if _checkadmin(update,1) == False:
        return
    
    og = args[0]
    points = args[1]
    
    if len(args) != 2 or og.isdigit() == False or points.isdigit() == False:
        update.message.reply_text('Please update points in the following format:\n/addpoints <OG> <Points>')
    else:
        current_points = int(pb.pb_read(og,"Points"))
        current_points += int(points)
        
        pb.pb_write(int(og),current_points,"Points")
        
        # Feedback to the command sender
        update.message.reply_text('Added {} points to OG {}!'.format(points, og))
        
        # Feedback to the OG
        try:
            bot.send_message(chat_id=OG_IDS_D[og],
                                 text="You have been awarded {} points!".format(points))
        except KeyError:
            update.message.reply_text('⚠️ OG IS NOT REGISTERED! ⚠️')
        

def checkallpoints(bot, update):
    
    if _checkadmin(update,1) == False:
        return
        
    """ Returns the Points of individual OGS to the requester """
    points_list = pb.pb_read("Points")

    msg_format = "OG {}: {}\n"
    msg = ""
    a = 1
    
    for i in range(1,25):
        
        msg += msg_format.format(a, points_list[i])
        a += 1
    
    update.message.reply_text(msg)

# =============================================================================
# LEVEL 0 COMMANDS
# =============================================================================
def checkpoints(bot, update):
    """ Returns the cumulative house points """
#    print(pb.pb_read("Points"))
    points_list = pb.pb_read("Points")
    print(points_list)
    fira = sum(points_list[1:7])
    silo = sum(points_list[7:13])
    kepa = sum(points_list[13:19])
    egro = sum(points_list[19:25])
    
    msg  = "🦁FIRA: {}\n🐥SILO: {}\n🦈KEPA: {}\n🐍EGRO: {}\n".format(fira,silo,kepa,egro)
          
    update.message.reply_text(msg)

# =============================================================================
# OTHER COMMANDS
# =============================================================================
    
def test(bot, update):
    bot.send_message(chat_id=-281335888,
                             text="DOORS ARE NOW OPEN!")

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def get_time(bot, update):
    """Returns Current Time in HH:MM"""
    time_now = time.strftime("%H:%M", time.gmtime())
    update.message.reply_text(time_now)

# =============================================================================
# PERIODIC JOBS
# =============================================================================


def p_start(bot, update):
    """ Initialize the repeating job """
    global job_minute
    job_minute = j.run_repeating(time_assignment, interval=5, first=0)
    
    
def p_stop(bot, update):
    """ Stop the repeating job """
    job_minute.schedule_removal()

# TESTING TIMINGS
cutoffs = ["14:25","14:26",
       "14:27","14:28",
       "05:00","05:02",
       "05:45","05:52",
       "06:30","06:33",
       "07:15","07:18",
       "07:40","07:43"]

# ACTUAL TIMINGS
#    cutoffs = ["04:00","04:03",
#           "04:30","04:32",
#           "05:00","05:02",
#           "05:45","05:52",
#           "06:30","06:33",
#           "07:15","07:18",
#           "07:40","07:43"]

def time_assignment(bot, job):
    """ Time Assignment for AMAZING RACE """


    msg = {14:"TIME BASED S U P P P RIISE CHALLENGE 1 (3 MINS)"
             "\nIf a deadline was due in 12 hours, what would an SUTD student do?"
             "\n\n   a) Go to Simpang and have Supper"
             "\n   b) Stay up till Dawn to complete the Work"
             "\n   c) Nothing, because he/she should have finished it long ago."
             "\n   d) Lie down, try not to cry, cry a lot."
             "\n   e) Rage at your teammates that don’t do work."
             "\n   f) All of the above",
           13:"TIME BASED CHALLENGE 1 HAS ENDED!",
           12:"TIME BASED S U P P P RIISE CHALLENGE 2 (2 MINS)"
             "\nWhere was SUTD’s campus initially located at?",
           11:"TIME BASED CHALLENGE 2 HAS ENDED!",
           10:"TIME BASED S U P P P RIISE CHALLENGE 3 (2 MINS)"
              "\nWhat was named after SUTD?"
              "\n\n   a) A Drone"
              "\n   b) A Mountain"
              "\n   c) 3D-Printer Model"
              "\n   d) A Hotel",
            9:"TIME BASED CHALLENGE 3 HAS ENDED!",
            8:"TIME BASED S U P P P RIISE CHALLENGE 4 (7 MINS)"
              '\nTake a video of one OG member successfully saying:'
              '“Kakak ku kata, kuku kaki ku kotor. Ku kikis kuku kotor kaki ku”.'
              'which is: “My sister said, my toenails are dirty. Then I shaped my dirty toenails” in Malay',
            7:"TIME BASED CHALLENGE 4 HAS ENDED!",
            6:"TIME BASED S U P P P RIISE CHALLENGE 5 (3 MINS)"
              "\nName the top 2 places to scavenge for materials in SUTD.",
            5:"TIME BASED CHALLENGE 5 HAS ENDED!",
            4:"TIME BASED S U P P P RIISE CHALLENGE 6 (3 MINS)"
              "\nWhat makes your day?",
            3:"TIME BASED CHALLENGE 6 HAS ENDED!",
            2:"TIME BASED S U P P P RIISE CHALLENGE 7 (3 MINS)"
              "1_,  2_,  3_,  4 _______,  5th ___",
            1:"TIME BASED CHALLENGE 7 HAS ENDED!"
              "\n\nThat's all folks!"
           }
    time_now = time.strftime("%H:%M", time.gmtime())
    
    
    if time_now >= cutoffs[0]:
        for _id in OG_IDS:
            bot.send_message(chat_id=_id, text=msg[len(cutoffs)])
        
        cutoffs.pop(0)

def callback_minute(bot, job):
    bot.send_message(chat_id=333643163, 
                     text='One message every minute')

# =============================================================================
# MAIN BOT
# =============================================================================

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(AuthKey)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("addpoints", addpoints, pass_args=True))
    dp.add_handler(CommandHandler("checkpoints", checkpoints))
    dp.add_handler(CommandHandler("checkallpoints", checkallpoints))
    dp.add_handler(CommandHandler("adminaccess", adminaccess, pass_args=True))
    dp.add_handler(CommandHandler("registerog", registerog, pass_args=True))
    dp.add_handler(CommandHandler("configuredoors", configuredoors))
    dp.add_handler(CommandHandler("refreshdata", refreshdata))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("time", get_time))
    dp.add_handler(CallbackQueryHandler(_button))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    # updater = Updater(..)

    # PERIODIC JOBS
    global j
    j = updater.job_queue
    
    dp.add_handler(CommandHandler("p_start", p_start))
    dp.add_handler(CommandHandler("p_stop", p_stop))
    
    # log all errors
    dp.add_error_handler(_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
