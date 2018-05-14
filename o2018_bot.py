#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# VERSION 1.25
# Commented
# =============================================================================
"""Official Orientation 2018 Telegram Bot.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError
import read_write_to_firebase as pb
import logging
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Get Admin/Execs List
# Admin List
admins = pb.pb_read("Admins")
admins = list(admins.values())

# Executives List
execs = pb.pb_read("Execs")
execs = list(execs.values())
execs.extend(admins)

# Dictionary where key = security level, value = list of authorised users
security = {2:admins,1:execs}

# Default ID to receive amazing race answers
answer_receiver_id = 260974669

# Get OG IDS from firebase as dictionary
OG_IDS_D = pb.pb_read("OG_IDS")
OG_IDS_D = {k:v for k,v in enumerate(OG_IDS_D)}

# Reverse dictionary of OG IDS
OG_IDS_D_rev = {v: k for k,v in OG_IDS_D.items()}
OG_IDS = list(OG_IDS_D.values())

# Default Weather
weather_d = {"SUTD":"Location 1 (SU): ☀️",
             "Ubi":"Location 2 (U): ☀️",
             "Dakota":"Location 3 (D): ☀️",
             "Stadium":"Location 4 (S): ☀️",
             "Gardens by the Bay":"Location 5 (G): ☀️"
             }

# Telegram bot Auth Key
AuthKey = "566390966:AAEPvfBKfUhb1eSct9Ty1lseKHPfzHgfQWQ"

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

# =============================================================================
# HOUSEKEEPING COMMANDS begin the command with _
# =============================================================================

def _checkadmin(update, level):
    """ Check if command sender has enough priviliege """
    
    # Get command sender id
    user = update.message.chat.id
    
    # Feedback to command sender if they do not have enough privilege
    if user not in security[level]:
        update.message.reply_text("You do not have enough privilege!")
        return False

def _button(bot, update):
    
    # Callback dictionary
    callback = {1:'DOORS OPEN',
                2:'DOORS CLOSED',
                3:'Location 1 (SU): ☀️',
                4:'Location 2 (U): ☀️',
                5:'Location 3 (D): ☀️',
                6:'Location 4 (ST): ☀️',
                7:'Location 5 (G): ☀️',
                8:'Location 1 (SU): 🌧',
                9:'Location 2 (U): 🌧',
                10:'Location 3 (D): 🌧',
                11:'Location 4 (ST): 🌧',
                12:'Location 5 (G): 🌧',
                }
    
    # Get callback data from button press
    query = update.callback_query
    query_num = int(query.data)
    
    # Open doors function for maze runner game
    def open_doors(bot, update):
        for _id in OG_IDS:
            try:
                bot.send_message(chat_id=_id,
                                 text="⚠️ DOORS ARE NOW OPEN! ⚠️")
            except:
                pass
            
    # Close doors function for maze runner game
    def close_doors(bot,update):
        for _id in OG_IDS:
            try:
                bot.send_message(chat_id=_id,
                                 text="⚠️ WARNING! DOORS ARE NOW CLOSED! ⚠️")
            except:
                pass
    
    # Updates weather for amazing race
    def weather_buttons(bot, update, query_num):
        if query_num == 3 or query_num == 8:
            weather_d["SUTD"] = callback[query_num]
        elif query_num == 4 or query_num == 9:
            weather_d["Ubi"] = callback[query_num]
        elif query_num == 5 or query_num == 10:
            weather_d["Dakota"] = callback[query_num]
        elif query_num == 6 or query_num == 11:
            weather_d["Stadium"] = callback[query_num]
        elif query_num == 7 or query_num == 12:
            weather_d["Gardens by the Bay"] = callback[query_num]
    
    # Query Handler
    if query_num == 1:
        open_doors(bot, update)
    elif query_num == 2:
        close_doors(bot, update)
    elif 3 <= query_num <= 12:
        weather_buttons(bot, update, query_num)
    
    # Feedback to button presser
    bot.edit_message_text(text="Selected option: {}".format(callback[query_num]),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def _error(bot, update, error):
    """ Error handler """
    
    try:
        raise error
    except ChatMigrated as e:
        print(e.new_chat_id)
        return e.new_chat_id
        
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    

# =============================================================================
# REGISTRATION
# =============================================================================

def adminaccess(bot, update, args):
    """ User Input: /adminaccess <password>"""
    """ args[0] = <password> """
    """ Adds user to admin/execs whitelist """
    
    # Check correct number of arguments
    if len(args) != 1:
        
        # Feedback if wrong number of arguments
        update.message.reply_text('Request admin by the following format:\n/adminaccess <password>')
    else:
        # Feedback if correct number of arguments
        # Get command sender user id
        user_id = update.message.chat.id
        
        # Grant Admin access
        if args[0] == "adminme9999":
            pb.pb_write(user_id,user_id,"Admins")
            update.message.reply_text("You are granted Level 2 Access")
        
        # Grant Exec Access
        elif args[0] == "adminme0905":
            pb.pb_write(user_id,user_id,"Execs")
            update.message.reply_text("You are granted Level 1 Access")
            
        # Invalid Password
        else:
            update.message.reply_text("Invalid Password!")

def registerog(bot, update, args):
    """ User Input: /registerog <OG>"""
    """ args[0] = <OG> """
    """ Registers OG to the system """
    OG_IDS = int(args[0])
    
    # Check correct number of arguments
    if len(args) != 1:
        
        # Feedback if wrong number of arguments
        update.message.reply_text('Register your OG telegram group using the following format:\n/registerog <OG #>')
    else:
        
        # Check if OG is a allowed number (1-24)
        if OG_IDS not in list(range(1,25)):
            update.message.reply_text("Please enter a OG Number from 1-24!")
            return
        
        # Check if OG is already registered
        if str(OG_IDS) in list(pb.pb_read("OG_IDS")):
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
def broadcast(bot, update, args):
    """ Broadcast a message to all OG groups """
    if _checkadmin(update,2) == False:
        return
    
    msg = args[0]
    
    # Preset Messages
    if msg == '!1':
        msg = """
        Hi freshies! there's a competition ongoing for secret partner. Take a photo with your SP and stand a chance to win great prizes!
\n\n1) The most creative SP post will stand a chance to win an $80 meal voucher for 2
\n2) Couple photo with the highest number of likes will receive $40 Capitaland vouchers
\n\nSubmissions and like count ends 12th May 1800hrs
\n\nHashtag #sutdorientationSP2018 for submission and make sure the account is not private.
"""
    elif msg == '!2':
        msg = """
        📣THE AMAZING RACE HAS STARTED‼️
\n🏃🏿🏃🏽🏃🏻🏃🏼‍♀️🏃🏼🏃🏻‍♀️🏃🏾🏃🏾‍♀️🏃🏽‍♀️🏃🏽🏃🏻‍♀️🏃🏾‍♀️🚶🏻
"""
    elif msg == '!3':
        msg = """
        For the In-school challenge where you need to find the Camp Execs for the puns: They can be found outside ISH, there are three of them. 
\n\nFor the In-school challenge where you need to pronounce the very long word, the link is https://bit.ly/2FKFZq7
"""
    else:
        msg = " ".join(map(str,args))
     
    # Send Message to all OG Chats
    for _id in OG_IDS:
        try:
            bot.send_message(chat_id=_id,
                             text=msg)
        except:
            update.message.reply_text("ERROR: {}".format(OG_IDS_D_rev[_id]))

def refreshdata(bot, update):
    """ Refresh the admin/executive list in the bot """
    if _checkadmin(update,2) == False:
        return
    
    admins = pb.pb_read("Admins")
    admins = list(admins.values())
    execs = pb.pb_read("Execs")
    execs = list(execs.values())
    execs.extend(admins)
    OG_IDS = list(pb.pb_read("OG_IDS"))
    update.message.reply_text("ADMINS:\n{}\n\nEXECS:\n{}\n\nOG IDS:\n{}".format(admins,execs,OG_IDS))
    global security
    security = {}
    security = {2:admins,1:execs}

def configuredoors(bot, update):
    """ Sends the Door status message to all OGS for Mutant Game"""
    
    # Check admin privilege
    if _checkadmin(update,1) == False:
        return
    
    # Creates the inline keyboard layout
    # Each inner bracket is a new line of buttons
    keyboard = [[InlineKeyboardButton("OPEN DOORS", callback_data=1),
                 InlineKeyboardButton("CLOSE DOORS", callback_data=2)]]

    # Creates the inline keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Sends the inline keyboard to the user
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def receiveanswers(bot, update):
    """ Become the answer receiver for amazing race """
    
    if _checkadmin(update,2) == False:
        return
    
    global answer_receiver_id
    answer_receiver_id = update.message.chat.id

    update.message.reply_text("You will now receive the OG answers for Amazing Race!")

# =============================================================================
# LEVEL 1 (EXECS) COMMANDS
# =============================================================================
def addpoints(bot, update, args):
    """ User Input: /addpoints <OG> <Points> """
    """ args[0] = <OG> args[1] = <Points> """
    """ Updates points in firebase """
    
    # Check admin privileges
    if _checkadmin(update,1) == False:
        return
    
    # Input Validation
    if len(args) != 2:
        update.message.reply_text('Please update points in the following format:\n/addpoints <OG> <Points>')
        return
    
    # Label variables
    og = args[0]
    points = args[1]
    
    # Convert points input to integer
    # Input Validation
    try:
        points = int(points)
    except ValueError:
        update.message.reply_text('Please update points in the following format:\n/addpoints <OG> <Points>')
        return
    
    # Input Validation
    if len(args) != 2 or og.isdigit() == False or type(points) != int:
        update.message.reply_text('Please update points in the following format:\n/addpoints <OG> <Points>')
        return
    else:
        
        # Add points to firebase
        current_points = int(pb.pb_read(og,"Points"))
        current_points += int(points)
        pb.pb_write(int(og),current_points,"Points")
        
        # Feedback to the command sender
        # + POINTS
        if points >= 0:
            if points == 1:
                msg = '+{} point to OG {}!'
            else:
                msg = '+{} points to OG {}!'
                
        # - POINTS
        if points < 0:
            if points == -1:
                msg = '{} point from OG {}!'
            else:
                msg = '{} points from OG {}!'
       
        # Feedback message to sender
        update.message.reply_text(msg.format(points, og))
        
        # Feedback to the OG (only if added points)
        try:
            if points > 0:
                bot.send_message(chat_id=OG_IDS_D[int(og)],
                                     text="You have been awarded {} points!".format(points))
        except KeyError:
            # Feedback message to sender if OG is not registered.
            update.message.reply_text('⚠️ OG IS NOT REGISTERED! ⚠️')
            

def addpointsh(bot, update, args):
    """ User Input: /addpoints <house> <Points> """
    """ args[0] = <OG> args[1] = <Points> """
    """ Updates house points in firebase """
    houses_d = {'fira':[1,2,3,4,5,6],
                'silo':[7,8,9,10,11,12],
                'kepa':[13,14,15,16,17,18],
                'egro':[19,20,21,22,23,24]}
    
    houses = ['fira','silo','kepa','egro']
    
    err_msg = 'Please update points to house in the following format:\n/addpointsh <house> <Points>'
    
    # Check admin privileges
    if _checkadmin(update,1) == False:
        return
    
    # Input Validation
    if len(args) != 2:
        update.message.reply_text(err_msg)
        return
    
    house = args[0]
    points = args[1]
    
    # Convert input to integer
    # Input Validation
    try:
        points = int(points)
    except ValueError:
        update.message.reply_text(err_msg)
    
    # Input Validation
    if len(args) != 2 or house not in houses or type(points) != int:
        update.message.reply_text(err_msg)
        return
    else:
        # Add/Minus points to firebase
        current_points = int(pb.pb_read(house,"Points_H"))
        current_points += int(points)
        pb.pb_write(house,current_points,"Points_H")
        
        # Message to the command sender
        if points >= 0:
            if points == 1:
                msg = '+{} point to {}!'
            else:
                msg = '+{} points to {}!'
            
        if points < 0:
            if points == -1:
                msg = '{} point from {}!'
            else:
                msg = '{} points from {}!'
       
        # Feedback to command sender
        update.message.reply_text(msg.format(points, house))
        
        # Feedback to all OGs in House (only if added points)
        try:
            if points > 0:
                for i in houses_d[house]:
                    bot.send_message(chat_id=OG_IDS_D[i],
                                         text="{} has been awarded {} points!".format(house, points))
        except KeyError:
            update.message.reply_text('⚠️ OG IS NOT REGISTERED! ⚠️')
    
def checkallpoints(bot, update):
    """ Returns the Points of individual OGS to the requester """
    
    # Check Admin Privileges
    if _checkadmin(update,1) == False:
        return
        
    # Get points of each og from firebase
    points_list = pb.pb_read("Points")

    # Output message format
    msg_format = "OG {}: {}\n"
    
    # Initialise output message
    msg = ""
    
    # OG Counter
    a = 1
    
    # Generate Response
    for i in range(1,25):
        
        msg += msg_format.format(a, points_list[i])
        a += 1
    
    # Output message response
    update.message.reply_text(msg)

def updateweather(bot, update):
    
    # Check admin privileges
    if _checkadmin(update,1) == False:
        return
    
    # Buttons
    keyboard = [[InlineKeyboardButton("SUTD ☀️", callback_data=3)],
                [InlineKeyboardButton("Ubi ☀️", callback_data=4)],
                [InlineKeyboardButton("Dakota ☀️", callback_data=5)],
                [InlineKeyboardButton("Stadium ☀️", callback_data=6)],
                [InlineKeyboardButton("Gardens by the Bay ☀️", callback_data=7)],
                [InlineKeyboardButton("SUTD 🌧", callback_data=8)],
                [InlineKeyboardButton("Ubi 🌧", callback_data=9)],
                [InlineKeyboardButton("Dakota 🌧", callback_data=10)],
                [InlineKeyboardButton("Stadium 🌧", callback_data=11)],
                [InlineKeyboardButton("Gardens by the Bay 🌧", callback_data=12)]]
    
    # Create and display inline keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def weather(bot,update):
    """ Check Weather at Amazing Race Locations """
    weather_data = list(weather_d.values())
    
    msg = "Weather Updates:"
    msg += "\n {}\n {}\n {}\n {}\n {}".format(*weather_data)
    
    update.message.reply_text(msg)

# =============================================================================
# LEVEL 0 COMMANDS
# =============================================================================
def checkpoints(bot, update):
    """ Returns the cumulative house points """
    
    # Get ID of sender
    ogid = update.message.chat.id
    
    points_list = pb.pb_read("Points")
    points_list_house = pb.pb_read("Points_H")
    fira = sum(points_list[1:7])
    fira += points_list_house['fira']
    silo = sum(points_list[7:13])
    silo += points_list_house['silo']
    kepa = sum(points_list[13:19])
    kepa += points_list_house['kepa']
    egro = sum(points_list[19:25])
    egro += points_list_house['egro']
#    x = "̡͙̬̻̤̺̲̦̝͙ͅs͈̱̮̠̳͈͡ e̗͔̝ ̺̝͖̟̘̺̮c͕͢ ̦̞̗͜r̖͖͍̪ ̙e̛ ̮͈̬̤t̛̖͓ͅ"
    
    # Additional line to indicate OG Number and respective points if message was sent by OG
    try:
        og = int(OG_IDS_D_rev[ogid])
        og_msg = "\n\nOG {}: {}".format(og,points_list[og])

    except KeyError:
        og_msg = ""
        
    msg  = "🦁FIRA: {}\n🐥SILO: {}\n🦈KEPA: {}\n🐍EGRO: {}".format(fira,silo,kepa,egro)
#    msg  = "🦁FIRA: {}\n🐥SILO: {}\n🦈KEPA: {}\n🐍EGRO: {}".format(x,x,x,x)
    msg += og_msg
    
    # Output message
    update.message.reply_text(msg)
    
def answer(bot, update):
    """ Forwards answer to message receiver """
    
    # Get sender chat id/message id
    answer_msg_id = update.message.message_id
    answer_chat_id = update.message.chat.id
    
    # Forward Message to message receiever
    if answer_chat_id in OG_IDS or answer_chat_id in admins:
        try:
            # Tags submission by OG
            msg = "===OG #{} Submission===".format(OG_IDS_D_rev[answer_chat_id])
            bot.send_message(answer_receiver_id, text=msg)
        except KeyError:
            pass
        bot.forward_message(answer_receiver_id,answer_chat_id,answer_msg_id)
        update.message.reply_text("Your answer has been submitted!")
    else:
        update.message.reply_text("You can only submit answers through the OG Chat!")


def answer_photo(bot, update):
    """ Photo/Video answer Handler """
    
    # Get sender chat id/message id
    answer_msg_id = update.message.message_id
    answer_chat_id = update.message.chat.id
    
    # In the event of photo/video answer
    check = update.message.parse_caption_entities()
    check_list = list(check.values())

    # Forward Message to message reciever
    if check_list != [] and (answer_chat_id in OG_IDS or answer_chat_id in admins):
        
        # Input verification
        if check_list[0] == "/answer":
            try:
                # Tag submission by OG
                msg = "===OG #{} Submission===".format(OG_IDS_D_rev[answer_chat_id])
                bot.send_message(answer_receiver_id, text=msg)
            except KeyError:
                pass
            
            # Forward Message
            bot.forward_message(answer_receiver_id,answer_chat_id,answer_msg_id)
            
            # Feedback to answer sender
            update.message.reply_text("Your answer has been submitted!")
    
# =============================================================================
# OTHER COMMANDS
# =============================================================================
    
def test(bot, update):
    print(update.message.chat.id)

def echo(bot, update):
    """Echo the user message."""
    
    # Check if sender is not a group
    if int(update.message.chat.id) > 0:
        update.message.reply_text(update.message.text)

def get_time(bot, update):
    """Returns Current Time in HH:MM"""
    time_now = time.strftime("%H:%M", time.gmtime())
    update.message.reply_text(time_now)

def sendnudes(bot, update):
    """b00bs"""
    update.message.reply_text("(  .  )(  .  )")

# =============================================================================
# PERIODIC JOBS
# =============================================================================


def p_start(bot, update):
    """ Initialize the repeating job """
    global job_minute
    job_minute = j.run_repeating(time_assignment, interval=5, first=0)
    update.message.reply_text("Time Based Challenges is now ACTIVE!")
    
def p_stop(bot, update):
    """ Stop the repeating job """
    job_minute.schedule_removal()
    update.message.reply_text("Time Based Challenges is now DEACTIVATED!")

# TESTING TIMINGS
#cutoffs = ["14:25","14:26",
#       "14:27","14:28",
#       "05:00","05:02",
#       "05:45","05:52",
#       "06:30","06:33",
#       "07:15","07:18",
#       "07:40","07:43"]

# ACTUAL AMAZING RACE TIMINGS
cutoffs = ["04:10","04:13",
       "04:40","04:42",
       "05:10","05:12",
       "05:55","06:02",
       "06:40","06:43",
       "07:25","07:28",
       "07:50","07:53"]

def time_assignment(bot, job):
    """ Time Assignment for AMAZING RACE """


    msg = {14:"🕑 TIME BASED S U P P P RIISE CHALLENGE 1 (3 MINS)"
             "\nIf a deadline was due in 12 hours, what would an SUTD student do?"
             "\n\n   a) Go to Simpang and have Supper"
             "\n   b) Stay up till Dawn to complete the Work"
             "\n   c) Nothing, because he/she should have finished it long ago."
             "\n   d) Lie down, try not to cry, cry a lot."
             "\n   e) Rage at your teammates that don’t do work."
             "\n   f) All of the above",
           13:"TIME BASED CHALLENGE 1 HAS ENDED!",
           12:"🕑 TIME BASED S U P P P RIISE CHALLENGE 2 (2 MINS)"
             "\nWhere was SUTD’s campus initially located at?",
           11:"TIME BASED CHALLENGE 2 HAS ENDED!",
           10:"🕑 TIME BASED S U P P P RIISE CHALLENGE 3 (2 MINS)"
              "\nWhat was named after SUTD?"
              "\n\n   a) A Drone"
              "\n   b) A Mountain"
              "\n   c) 3D-Printer Model"
              "\n   d) A Hotel",
            9:"TIME BASED CHALLENGE 3 HAS ENDED!",
            8:"🕑 TIME BASED S U P P P RIISE CHALLENGE 4 (7 MINS)"
              '\nTake a video of one OG member successfully saying:'
              '“Kakak ku kata, kuku kaki ku kotor. Ku kikis kuku kotor kaki ku”.'
              'which is: “My sister said, my toenails are dirty. Then I shaped my dirty toenails” in Malay',
            7:"TIME BASED CHALLENGE 4 HAS ENDED!",
            6:"🕑 TIME BASED S U P P P RIISE CHALLENGE 5 (3 MINS)"
              "\nName the top 2 places to scavenge for materials in SUTD.",
            5:"TIME BASED CHALLENGE 5 HAS ENDED!",
            4:"🕑 TIME BASED S U P P P RIISE CHALLENGE 6 (3 MINS)"
              "\nWhat makes your day?",
            3:"TIME BASED CHALLENGE 6 HAS ENDED!",
            2:"🕑 TIME BASED S U P P P RIISE CHALLENGE 7 (3 MINS)"
              "1_,  2_,  3_,  4 _______,  5th ___",
            1:"TIME BASED CHALLENGE 7 HAS ENDED!"
              "\n\nThat's all folks!"
           }
    
    # Get Current Time
    time_now = time.strftime("%H:%M", time.gmtime())
    
    if time_now >= cutoffs[0]:
        for _id in OG_IDS:
            try:
                bot.send_message(chat_id=_id, text=msg[len(cutoffs)])
            except:
                pass
        
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

    # Telegram Commands / Command Handlers
    dp.add_handler(CommandHandler("addpoints", addpoints, pass_args=True))
    dp.add_handler(CommandHandler("addpointsh", addpointsh, pass_args=True))
    dp.add_handler(CommandHandler("checkpoints", checkpoints))
    dp.add_handler(CommandHandler("checkallpoints", checkallpoints))
    dp.add_handler(CommandHandler("adminaccess", adminaccess, pass_args=True))
    dp.add_handler(CommandHandler("registerog", registerog, pass_args=True))
    dp.add_handler(CommandHandler("configuredoors", configuredoors))
    dp.add_handler(CommandHandler("refreshdata", refreshdata))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("time", get_time))
    dp.add_handler(CommandHandler("answer", answer))
    dp.add_handler(CommandHandler("sendnudes", sendnudes))
    dp.add_handler(CommandHandler("receiveanswers", receiveanswers))
    dp.add_handler(CommandHandler("updateweather", updateweather))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("broadcast", broadcast, pass_args=True))
    dp.add_handler(CallbackQueryHandler(_button))
    
    # Non-commands / Message Handlers
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, answer_photo))
    dp.add_handler(MessageHandler(Filters.video, answer_photo))
    
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
