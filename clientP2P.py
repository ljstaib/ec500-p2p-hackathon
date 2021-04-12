#!/usr/bin/env python3
#Adapted from https://stackoverflow.com/questions/21233340/sending-string-via-socket-python for educational purposes

#Luke Staib, ljstaib@bu.edu, 2021

import socket
import pymongo
import datetime

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')

db = client['test']
HOST = '155.41.17.114'
PORT = 5000
print(db)
#Client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

def msg_funct(msg, socket):
   socket.send(msg.encode()) 
   data = socket.recv(1024).decode()
   print('User 2 sent: ', data)
   db.messages.insert_one(
        {
        "Sender" : "Bob",
        "Receiver" : "Alice",
        "Text" : data,
        "Timestamp" : datetime.datetime.now()
        }
    )

while True:
	msg = input('Enter a message: ')
	msg_funct(msg, s)

s.close()
