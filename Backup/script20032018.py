#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kenghin
"""
import requests
import telepot
import time
import numpy as np

#list of temp OGs that I would want to send info to
###########OG1########2##########3##########4############
tempOGs = [-243939426,-296907230,-264240628,-272853588]
oglOGs = {1:-222728972, 2:-303352307, 3:-298030907, 4:-251151309}
oglOGs_names = {1:"KEPA", 2:"FIRA", 3:"ERGO", 4:"SILO"}
OGs = [-216431029,-281335888,-294969153,-211493732,-263226255,-304846653,-302635765,-309627168,-246266570,-252214507,-285626938,-261931371,-265552120,-233736257,-279459888,-262612692,-265434384,-270934465,-306607047,-300270851,-305819035,-266950288,-318797760,-316416695]
admins = [333643163,298612657,222809708,345917322,31225422,202001285,287175512,247670505,155369046,139515342]
# TODO: add welfare to admin
"""
--- OGL GROUPS ---
1. SILO -222728972
2. EGRO -303352307
3. KEPPA -298030907
4. FIRA -251151309


--- OCOMM ---
Keng Hin 333643163
Qiaorou 155369046
Ali 139515342

---Camp Executives---
Wenkie 298612657
Jian Wei 222809708
Junhan 345917322
Wong 31225422
Caleb 202001285
Adam 287175512
Jane 247670505

"""
tasks =  {1:"CHALLENGE NAME: Gotta’ Catch ‘em Nuclear Snakes on a Plane!"
            "\n\n Air travel was once a major driver of global development,"
            "but recent findings point to the scary possibility that it led "
            "to this nuclear disaster. Now a rare sight, catch one as it flies past."
            "\n\n Entire OG to take a jump shot with a flying aeroplane. Photo to be taken by OGL."
            "\n\n POINTS AWARDED: 30",
          2:"CHALLENGE NAME: Human Letters in the Sand!"
            "\n\n Help may never arrive, but you must be ready when it does, "
            "if it does. Practise your distress signal for when a rescue "
            "aircraft travels overhead."
            "\n\n Entire OG to take a jump shot with a flying aeroplane. Photo to be taken by OGL."
            "\n\n POINTS AWARDED: 20",
          3:"CHALLENGE NAME: If You cannot Convince them, Confuse them!"
            "\n\n  Interrogation is a skill employed to extract valuable "
            "information from you, but confusing your interrogator is a "
            "fine art in itself. Will you be the con-artist our team needs "
            "to survive in this cruel world."
            "\n\n Re-enact an OG member’s entrance interview with SUTD with a"
            "stuffed animal as the interviewer (voiced by another OG member)."
            "Student is to use unnecessarily bombastic vocabulary, while"
            "interviewer remains unimpressed. Two-minute video to be recorded by OGL."
            "\n\n POINTS AWARDED: 20",
          4:"CHALLENGE NAME: Last Man Staring!"
            "\n\n  Legend has it that our eyes are windows to our soul."
            "Stare deep enough and perhaps you can unravel the secret"
            "that can save all humanity, and it lies in your friend."
            "\n\n OG members pair up and stare at each other while keeping a"
            "straight face and without laughing. One-minute video to be taken by OGL."
            "\n\n POINTS AWARDED: 20",
          5:"CHALLENGE NAME: I Will Follow You into the Dark!"
            "\n\n  If you want to go fast, go alone. If you want to go far, go together."
            "We are not sure when this nuclear fallout will subside, but at least we"
            "have each other."
            "\n\n Entire OG tie shoelaces together, and walk one breadth of the field."
            "Video to be taken by OGL."
            "\n\n POINTS AWARDED: 30",
          6:"CHALLENGE NAME: Creeperzoid 9000!"
            "\n\n  Perhaps this is not the best time for lighthearted whimsy in the"
            "middle of a nuclear fallout, or perhaps it is."
            "\n\n Do a funny pose behind another OG without them noticing."
            "Photo to be taken by an OGL."
            "\n\n POINTS AWARDED: 40",
          7:"CHALLENGE NAME: Panic! at the Track!"
            "\n\n Hysteria fills the air; some of you may start experiencing panic attacks."
            "Save one another from this cruel world, before it is too late..."
            "\n\n One OG member ties a balloon to him/herself and runs one round"
            'around the SUTD track while hysterically screaming, "It’s following me!".'
            "Three other OG members are must chase after balloon boy/girl telling him/her"
            "that he/she is overreacting. Video to be taken by an OGL."
            "\n\n POINTS AWARDED: 40",
          8:"CHALLENGE NAME: How did they do that?!"
            "\n\n The wastelands has caused people to sound like they speak gibberish,"
            "but as a matter of fact they are not. You must be able to communicate with them."
            "\n\n Five member of the OG must successfully pronounce the word"
            "(longest city name in the world) in less than 5 seconds per person:"
            " Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch"
            "\n\n https://youtu.be/dCGkqUr1kbY?t=12s "
            "\n\n POINTS AWARDED: 40"}
           
tasks2 = {1:"CHALLENGE NAME: Let the Past Not be Past!"
            "\n\n In the earliest days of this dark, desolate world we live in today, "
            "looting and arson was widespread. The armed forces protected civilians "
            "from their own people, but their numbers quickly dwindled in the wake of "
            "the mounting chaos. Lest we forget."
            "\n\n Location: Dakota"
            "\n\n TASK 1: Remember the Kids! (120 pts)"
            "\n The bleak state of our post-apocalyptic world is depressing to say the least."
            "But we must stay strong, stay cheerful like when you were kids, never let this"
            "cruel world take our inner child away from us."
            "\n\n Locate the iconic dove playground in Dakota Crescent."
            "Snap 8 photos of OG members enjoying themselves either on the playground or playing"
            "various childhood games around the playground (e.g. Chopsticks, Zhar, Catching, etc.)."
            "Photos to be taken by OGLs."
            "\n\n TASK 2: Remember those who Protected Us! (120 pts)"
            "\n\n In the earliest days of this dark, desolate world we live in today, looting and arson was widespread. The armed forces protected civilians from their own people, but their numbers quickly dwindled in the wake of the mounting chaos. Lest we forget."
            "\n\n Locate the now-defunct Guillemard Camp, once home to the 1st Battalion, Singapore Infantry Regiment (1 SIR). Re-enact the most epic National Service stories, but with the ladies in the OG as the actors. Two-minute video to be taken by OGLs."
            "\n\n TOTAL POINTS AWARDED: 250",
           2:"CHALLENGE NAME: Pictionary Meets Survivor!"
            "\n\n Location: Sports Hub"
            "\n\n TASK 1: The Adventures of Flashback Boy & Decrypter Girl. (50 pts)"        
            "\n\n Legend has it that a young man will be bestowed the power of supernatural sight, and a young lady will be bestowed the power of supernatural knowledge. Apart, they are confused beings; but together, they could unravel the truths that we have all been blinded to."
            "\n\n One male OG member is starting to receive mysterious flashbacks. He needs to get these visions to a decrypter, who is a female OG member. However, flashback boy lives in SUTD hostel, while decrypter girl lives in Jurong West. The OGMs are tasked to accurately relay a message. from flashback boy to decrypter girl. The twist is that flashback boy relays the message to OGM 2 via hand gestures, OGM 2 relays the message to OGM 3 via whisper, OGM 3 relays the message to OGM 4 via hand gestures, etc. Finally, OGM 9 relays the message to decrypter girl via hand gestures, and she will tell her OGL what she believes the meaning behind the visions that flashback boy is having. "
            "\n\n TASK 2: The Writing on the Wall. (90 pts)"
            "\n\n Getting caught sending covert messages will land you an all-expense-paid tenure in prison, with a generous side of hard-labour. I think it’s time we practise some secret-message-sending madness."
            "\n\n OG members are given sentences and mathematical expressions of varying lengths and difficulties. Within a time limit of ten minutes, they must form as many of these phrase, using photos taken of signboards found all over the Sports Hub. Points will be given for whole words used, ‘building’ words using photos of separated alphabets of a word gives no points. "
            "\n\n Writing 1: Nuclear basketball; good fun. (18 pts)"
            "\n Writing 2: Nuclear swimming; no go. (18 pts)"
            "\n Writing 3: Indoor nuclear volleyball; cool. (18 pts)"
            "\n Writing 4: Nuclear beach volleyball; hot. (18 pts)"
            "\n Writing 5: Rising world forever; square wave (18 pts)"
            "\n\n TOTAL POINTS AWARDED: 150",
            3:"CHALLENGE NAME: Scout and Scavenge!"
            "\n\n Jalan Besar was the grandest repository of raw elemental gems prior to the nuclear fallout, crafters and smiths flocked from all over the world to score sick deals of rare gems. However, widespread nuclear contamination has left the place in shambles."
            "\n\n TASK 1: FIND THE LOCATIONS! (80 - 240 pts)"
            "\n OGs are given level one photo clues of shops that they need to find, as well a locality map demarcating the relative positions of the shops."
            "\n\n Upon successfully locating the shop, and taking a photo of the OG posing in front of the shop unit, our Telegram bot will send them a brief description of what useful things can be found in that particular shop."
            "\n\n However, if the OG is unable to locate the shop after 10 minutes, level two photo clue will be sent to them. After another 5 minutes, our final level three photo clue will be sent to them."
            "\n\n TOTAL POINTS AWARDED: 250",        
            4:"UBI-n to This Place??"
            "\n\n Ubi was the grandest repository of raw elemental gems prior to the nuclear fallout, crafters and smiths flocked from all over the world to score sick deals of rare gems. However, widespread nuclear contamination has left the place in shambles."
            "\n\n TASK 1: FIND THE LOCATIONS! (80 - 240 pts)"
            "\n OGs are given level one photo clues of shops that they need to find, as well a locality map demarcating the relative positions of the shops."
            "\n\n Upon successfully locating the shop, and taking a photo of the OG posing in front of the shop unit, our Telegram bot will send them a brief description of what useful things can be found in that particular shop."
            "\n\n However, if the OG is unable to locate the shop after 10 minutes, level two photo clue will be sent to them. After another 5 minutes, our final level three photo clue will be sent to them."
            "\n\n TOTAL POINTS AWARDED: 150",
            5:"Find the Tinkerer!"
            "\n\n TASK 1: Find the One! (130 pts)"
            "\n In order to survive the fallout, the players have to find the tinkerer to gain useful tips and tricks for the hard days ahead."
            "\n\n TASK 2: Cover and Concealment! (130 pts)"
            "\n Sometimes to survive in the wilderness, you need to adapt to the surroundings. Pretend to be part of the greenery there, take a photo and ensure that at least 3 members are inside and are hard to spot."
            "\n\n TASK 3: Jokes on Us! (130 pts)"
            "\n Even in the most dreadful situations, it never hurts to have some fun, take a touristy OG group photo. "
            "\n\n TOTAL POINTS AWARDED: 400"}

hints = {1:"https://ibb.co/gZWyoH",
         2:"https://ibb.co/fr7Gax",
         3:"https://ibb.co/fkxtNc", 
         4:"https://ibb.co/gucGax"}

hint_descriptions = {1:"This is a photo of the old Kallang Airport. The building in the background was the airport’s control tower at the time. For a period of time up to 2009, it was used as the HQ for the People’s Association. Today, what remains in the vicinity is the Old Airport Road market, where savoury hawker fare awaits.\n\n (10 pts)" ,
                     2:"This is a photo of the former National Stadium, where countless Singaporeans will recall National Day Parades, Singapore Youth Festival Opening Ceremonies, and Tiger Cup Finals being held. It is also the birthplace of the Kallang Roar.\n\n (10 pts)",
                     3:"This place is going to be your frequently visited place for the next 3.5 years.\n\n (10 pts)",
                     4:"The photo shows one of the places that you can visit in the area. Question: What is this place? Who designed this place?\n\n (10 pts)"}

"""
https://ibb.co/fr7Gax  -Airport Road
https://ibb.co/gucGax  -Former National Stadium
https://ibb.co/fkxtNc  -Gardens By the Bay
https://ibb.co/gZWyoH  -Jalan Besar
"""
# Unique token for the @o2018_bot
# RIP token = "488377854:AAEvKNuRAzdstZi543LRM6HunG5sVDxbJDc" #for oBot1
# RIP token = "487204285:AAEeMvu05bIySxe4MjVQxgDP9hPUyMe0fg4" #for oBot2
# RIP token = "510544520:AAGkl29HnONsmMsRlmAp5uhtrK2eAzor_eA"
# RIP token = "538219748:AAH-wR8hAtjbW5A5TqkG7GZoRab6_Rs97ek" 27 Feb - 28 Feb
# RIP token = "530705420:AAE8ofLk0AC6j9YTeHfrQXwtfUJVtVN_wlY" 28 Feb - 5 Mar
# RIP token = "552072621:AAGFjVgq1obGis592Wo-CRPfI6xY9kjsoXQ" 5 Mar - 7 Mar 2018
token = "566390966:AAEPvfBKfUhb1eSct9Ty1lseKHPfzHgfQWQ"

# initialize Bot
bot = telepot.Bot(token) 

# Unique URL to send commands to
url = "https://api.telegram.org/bot{0}/".format(token)

# Returns information from telegram server about the bot
def get_updates_json(request):
    getupdateurl = request + 'getUpdates'
    response = requests.get(getupdateurl,params='inline_query')
    return response.json()

print(bot.getUpdates())

# Returns information of the last sent message to the bot
def last_update(data):  
    results = data['result']
    if len(results) != 0:
        total_updates = len(results) - 1
    return results[total_updates]

# Returns the unique chat ID of whatever data is fed
def get_chat_id(data):  
    chat_id = data['message']['chat']['id']
    return chat_id

# Sends a message
def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def send_pic(chat, url):
    bot.sendPhoto(chat_id=chat, photo=url)

# Sends a ❤️ to everyone in the list
def send_love(id_list):
    text = "❤️ bot has been updated."
    for i in range(len(id_list)):
        send_mess(id_list[i], text)

# Returns all users that have connected to the bot
# Telegram does not keep the data on their server for more than 1 day
def connectedtobot(data):
    allcontacts = []
    results = data['result']
    for i in range(len(results)):
        try:
            if results[i]['message']['chat']['id'] not in allcontacts:
                allcontacts.append(results[i]['message']['chat']['id'])
        except KeyError:
            pass
    return allcontacts

# Collects User ID and Name and stores it into log.txt
def collectBasicinfo():
    chat_data = connectedtobot(get_updates_json(url))
    print(chat_data)
    time.sleep(4)
    print("writing to txtfile")
    open("log.txt","w")
    np.savetxt("log.txt",chat_data,fmt='%s')

# Starts the Bot
def activateBot():
    
    # Initialise Bot
    msgid = last_update(get_updates_json(url))["update_id"]
    pointsOG = {"1":1800,"2":950,"3":510,"4":1350}
    jailOG = {"1":0,"2":0,"3":0,"4":0}
    
    # Check for Admin Privilages
    def checkAdmin(user=0):
        if user in admins:
            return True
        else:
           send_mess(user, "Sorry, you cannot use that command!")
           return False
       
    ######### ---------- BOT COMMANDS (only when bot is activated) ---------- #########
    
    # Sends lists of Commands --------------------------------------------------
    def c_start(user=0,data=[]):
        print("Check.")
        #send_mess(user, "Hi, I am the official telegram bot for Orientation 2018! The current list of commands are: {}".format(commands_l))
        send_mess(user, user)
        return
    
    # Adds Points to specified OG (ADMIN COMMAND) ------------------------------
    def c_addpoints(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            group = str(data[1])
            points = int(data[2])
            pointsOG[group] += points
        except IndexError:
            send_mess(user, "Please add points using the following method: /addpoints,<OG>,<points>")
            return
        except KeyError:
            send_mess(user, "Only OG 1-4")
            return
        except ValueError:
            send_mess(user, "Please only enter integers!!")
            return
        send_mess(user, "Updated Points!")
        c_checkpoints(user,pointsOG)
    
    # Check Points of all OGs --------------------------------------------------
    def c_checkpoints(user=0,data=[]):
        flavour = "💎💎💎 OG POINTS 💎💎💎 \nOG1 {}: {} \nOG2 {}: {} \nOG3 {}: {}\nOG4 {}: {}".format(oglOGs_names[1],pointsOG["1"],oglOGs_names[2],pointsOG["2"],oglOGs_names[3],pointsOG["3"],oglOGs_names[4],pointsOG["4"])    
        send_mess(user, flavour)
 #                       "\nOG1 {}: {}"
 #                       "\nOG2 {}: {}"
 ##                       "\nOG3 {}: {}"
  #                      "\nOG4 {}: {}".format(oglOGs_names[1],pointsOG["1"])
                        #,oglOGs_names[2],pointsOG["2"],oglOGs_names[3],pointsOG["3"],oglOGs_names[4],pointsOG["4"])
    
    def c_sendmsg(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            myMessage = str(data[1])
        except IndexError:
            send_mess(user, "Please send message using the following method: /sendmsg,<text>")
            return
        for i in OGs:
#            send_mess(i, "{} says {}".format(user,myMessage))
            send_mess(i, myMessage)
            
    # View Task ----------------------------------------------------------------
    def c_task(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            print("Sending Task {} to {}".format(data[1],user))
            myMessage = str(tasks[int(data[1])])
        except KeyError:
            send_mess(user, "Only Task 1-8")
            return
        except IndexError:
            send_mess(user, "View challenges using the following method: /task,<task #>")
            return
        send_mess(user, myMessage)
      
    # Sends Tasks to all OGs ---------------------------------------------------    
    def c_sendtask(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            print("Sending Task {} to {}".format(data[2],user))
            recipient = oglOGs[int(data[1])]
            myMessage = str(tasks[int(data[2])])
        except KeyError:
            send_mess(user, "Only Task 1-8, OG 1-4")
            return
        except IndexError:
            send_mess(user, "Send challenges using the following method: /sendtask,<OG #>,<task #>")
            return
        send_mess(recipient, myMessage)
#        for i in OGs:
#            send_mess(i, myMessage)
            
    # View Task ----------------------------------------------------------------
    def c_task2(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            print("Sending Task {} to {}".format(data[1],user))
            myMessage = str(tasks2[int(data[1])])
        except KeyError:
            send_mess(user, "Only Task 1-8")
            return
        except IndexError:
            send_mess(user, "View outside challenges using the following method: /task2,<task #>")
            return
        send_mess(user, myMessage)
      
    # Sends Tasks to all OGs ---------------------------------------------------    
    def c_sendtask2(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            print("Sending Task {} to {}".format(data[2],user))
            myMessage = str(tasks2[int(data[2])])
            recipient = oglOGs[int(data[1])]
        except KeyError:
            send_mess(user, "Only Task 1-8")
            return
        except IndexError:
            send_mess(user, "Send outside challenges to OGs using the following method: /sendtask2,<og #>,<task #>")
            return
        send_mess(recipient, myMessage)
#        for i in OGs:
#           send_mess(i, myMessage)
            
    # View Hints ---------------------------------------------------    
    def c_hint(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            print("Sending Hint {} to {}".format(data[1],user))
            myUrl = str(hints[int(data[1])])
            myMsg = str(hint_descriptions[int(data[1])])
        except KeyError:
            send_mess(user, "Only Hint 1-4")
            return
        except IndexError:
            send_mess(user, "View hints using the following method: /hint,<hint #>")
            return
        send_pic(user, myUrl)
        send_mess(user, myMsg)
            
    # Sends Tasks to all OGs ---------------------------------------------------    
    def c_sendhint(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            print("Sending Hint {} to {}".format(data[2],user))
            recipient = oglOGs[int(data[1])]
            myUrl = str(hints[int(data[2])])
            myMsg = str(hint_descriptions[int(data[2])])
        except KeyError:
            send_mess(user, "Only Hint 1-4")
            return
        except IndexError:
            send_mess(user, "Send hints to OGs using the following method: /sendhint,<hint #>")
            return
        send_pic(recipient, myUrl)
        send_mess(recipient, myMsg)
        
#        for i in OGs:
#            send_pic(i, myUrl)
#            send_mess(i, myMsg)
            
    # Sends Tasks to all OGs ---------------------------------------------------    
    def c_addgpa(user=0,data=[]):
            send_mess(user, "Sorry can't help you with that!")
    
    # Insults Keane ------------------------------------------------------------        
    def c_insultkeane(user=0,data=[]):
            send_mess(user, "Keane sucks.")
            
    # Sends nudes --------------------------------------------------------------        
    def c_sendnudes(user=0,data=[]):
            send_mess(user, "(  .  )(  .  )")
    
    # Check Members in Jail ---------------------------------------------------- 
    def c_checkjail(user=0,data=[]):
        send_mess(user, "⛓⛓⛓ OGMs in Jail ⛓⛓⛓ \n OG1: {}\n OG2: {}\n OG3: {}\n OG4: {}".format(jailOG["1"],jailOG["2"],jailOG["3"],jailOG["4"]))
            
    # Add member to Jail -------------------------------------------------------        
    def c_jail(user=0,data=[]):
        if checkAdmin(user) == False:
            return
        try:
            print("Jailing member from OG {}".format(data[1],user))
            group = str(data[1])
            points = int(data[2])
            jailOG[group] += points
        except IndexError:
            send_mess(user, "Please jail using the following method: /addpoints,<OG>,<number jailed>")
            return
        except KeyError:
            send_mess(user, "Only OG 1-4")
            return
        except ValueError:
            send_mess(user, "Please only enter integers!!")
            return
        send_mess(user, "Updated Jail!")
        c_checkjail(user,jailOG)
        
    # Sends a door close message to all OGs ------------------------------------        
    def c_dooropen(user=0,data=[]):
        myMsg = "Doors are now open!"
        for i in tempOGs:
            send_mess(i, myMsg)
    
    # Sends a door close message to all OGs ------------------------------------
    def c_doorclose(user=0,data=[]):
        myMsg = "Doors are now close!"
        for i in tempOGs:
            send_mess(i, myMsg)
        
    # Dictionary of Commands
    commands_d = {"/start":c_start,
                  "/addpoints":c_addpoints,
                  "/checkpoints":c_checkpoints,
                  "/sendmsg":c_sendmsg,
                  "/task":c_task,
                  "/sendtask":c_sendtask,
                  "/task2":c_task2,
                  "/sendtask2":c_sendtask2,
                  "/hint":c_hint,
                  "/sendhint":c_sendhint,
                  "/addgpa":c_addgpa,
                  "/insultkeane":c_insultkeane,
                  "/sendnudes":c_sendnudes,
                  "/jail":c_jail,
                  "/checkjail":c_checkjail,
                  "/dooropen":c_dooropen,
                  "/doorclose":c_doorclose}

    # List of Commands from commands_d
    commands_l = list(commands_d.keys())
    
    while True:
        
        # Get essential updates
        current_data = last_update(get_updates_json(url))
        try:
            current_msgid = current_data["update_id"]
            lastsender = current_data["message"]["chat"]["id"]
            lastsender_name = current_data["message"]["chat"]["first_name"]
        except KeyError:
            current_msgid = current_data["message"]["message_id"]
            lastsender = current_data["message"]["chat"]["id"]
            lastsender_name = "???"
        # Update Dictionary of Commands with last sender
        # Allows bot to listen to the last message sent
        if msgid != current_msgid:
            # Get the latest Text
            try:
                recievedmsg = str(current_data["message"]["text"])
                basemsg = recievedmsg.split(",")
            except KeyError:
                recievedmsg = ""
                basemsg = "."
                pass
            # Splits the command into seperate parts, "," is the identifier
            print(lastsender_name,lastsender,": ",recievedmsg, basemsg[0])
            if basemsg[0] not in commands_l:
                send_mess(lastsender, "{} is not a valid command. Type /start to see all commands.".format(recievedmsg))
            else:
                print("Running {} command.".format(recievedmsg))
                time.sleep(1)
                # Activates Function written in command dictionary
                commands_d[basemsg[0]](lastsender,basemsg)
            msgid = current_msgid 
        
        # Set delay so anti lag
        print(".")
        time.sleep(0.5)
    
print(get_updates_json(url))

"""
---SAMPLE OF DATA---
{'update_id': 151568260, 'message':
    {'message_id': 265, 'from':
        {'id': 333643163, 'is_bot': False, 'first_name': 'Keng Hin',
         'username': 'kenghin', 'language_code': 'en-SG'},
     'chat': {'id': 333643163, 'first_name': 'Keng Hin',
              'username': 'kenghin', 'type': 'private'},
     'date': 1519694193, 'text': 'Hello'}}
"""
# List of people who are connected to the bot
people = connectedtobot(get_updates_json(url))

#send_love(people)
#collectBasicinfo()
print("Bot ACTIVE. Listenning for commands...")  
activateBot()
