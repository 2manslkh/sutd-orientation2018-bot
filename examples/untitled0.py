# -*- coding: utf-8 -*-
"""
Created on Fri May  4 14:16:58 2018

@author: kengh
"""
import datetime
import time

mlist = [1,2,3,4,5,6,7,8,9]
cutoffs = ["04:00","04:03",
           "04:30","04:32",
           "05:00","05:02",
           "05:45","05:52",
           "06:30","06:33",
           "07:15","07:18",
           "07:40","07:43"]

print(mlist[0:6])
print(mlist[6:8])
#print(datetime.datetime.now())
#now = datetime.datetime.now()
print(time.localtime())
now1 = time.strftime("%H:%M",time.localtime())
now1 = time.strptime(now1, "%H:%M")
time1 = time.strptime(cutoffs[0], "%H:%M")
time2 = time.strptime(cutoffs[1], "%H:%M")
print(now1)
print(time1)
print(now1 < time1)

class machinelearn():
    def __init__(x):
        self.x = x
        
a = machinelearn()
    