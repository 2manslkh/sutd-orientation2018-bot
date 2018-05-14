# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 21:59:14 2018

@author: kengh
"""

import pyrebase

# Initialize pyrebase

config = {
  "apiKey": "6UzJNNKWfMziGAtmqIbRqG9HtMYL3tYJR6wmA7uz",
  "authDomain": "o2018-bot.firebaseapp.com",
  "databaseURL": "https://o2018-bot.firebaseio.com/",
  "storageBucket": "o2018-bot.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()
# Write to firebase
def pb_write(key, value=0, group=""):
    if group != "":
        return db.child(group).update({key:value})
    else:
        return db.update({key:value})

# Writes to firebase with unique ID in main branch
def pb_writenew(value):
	return db.push(value)

# Read from firebase
def pb_read(key, group=""):
    if group == "":
        return db.child(key).get().val()
    else:
        return db.child(group).child(key).get().val()

# Wipes entire database
def pb_wipe():
	while True:
		confirm = input("Are You Sure? [Y/N]")
		if confirm == "Y":
			database = db.get()
			for data in database.each():
				db.child(data.key()).remove()
				print("Database wiped!")
			return
		if confirm == "N":
			print("Cancelled wipe")
			return

# Prints the entire database 
def pb_read_all():
	database = dict(db.get().val())
	print("Printing all data...")
	def read_level(d,indent=0):
		d_keys = list(d.keys())
		a = str(max([len(x) for x in d_keys]) + indent) # Returns length of longest string in list
		for key in d_keys:
			if type(d[key]) != dict:
				toprint = "{:>" + a + "}: {}"
				print(toprint.format(key,d[key]))
			else:
				toprint = "{:>" + a + "}"
				print(toprint.format(key))
				read_level(d[key],int(a))
				read_level(database)
                    