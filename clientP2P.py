#!/usr/bin/env python3
#Adapted from https://stackoverflow.com/questions/21233340/sending-string-via-socket-python for educational purposes

#Luke Staib, ljstaib@bu.edu, 2021

import socket
from threading import *
import pymongo
import datetime
import urllib.request, json

#discovery inits
discoveryclient = pymongo.MongoClient('mongodb+srv://Brian:cyp1b1@cluster0.v056q.mongodb.net/FileDB?retryWrites=true&w=majority')
discoverydb = discoveryclient['FileDB']
collection = discoverydb['Users']

#local message storage init
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')
db = client['test']

#Auto update IP
ipv4 = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read())
Name = input("Who are you?")
collection.update_one({"Name" : Name}, {"$set" : {"IP" : ipv4["ip"]}})

#Discovery
#print discoverable users
friends = collection.find({"Discoverable" : True})

for person in friends:
    print(person["Name"])

receiver = input("Whom would you like to talk to? Please choose from the list above:")
receiverDoc = collection.find_one({"Name" :{"$eq" : receiver}})

#Dynamic Host
#HOST = receiverDoc["IP"]
#print("HOST: ", HOST)

HOST = '127.0.0.1'
PORT = 5000

#Client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#UPDATE SENDER AND RECEIVER TO BE DYNAMIC + LIST ALL MESSAGES
#pastmessages = db.messages.find({"$or" : [{"$and" : [{"Sender" : Name}, {"Receiver" : receiver}]}, {"$and" : [{"Sender" : receiver },{"Receiver" : Name}]}]})
# for messages in pastmessages:
#     print("[", messages["Timestamp"],"] ", messages["Sender"], ": ",messages["Text"] )

def msg_funct(msg, socket):
   socket.send(msg.encode()) 
   data = socket.recv(1024).decode()
   print(receiver,' sent: ', data)

   
   #save received message
   db.messages.insert_one(
       {
            "Sender" : receiver,
            "Receiver" : Name,
            "Text" : data,
            "Timestamp" : datetime.datetime.now()
        })

   db.messages.insert_one(
        {
            "Sender" : Name,
            "Receiver" : receiver,
            "Text" : msg,
            "Timestamp" : datetime.datetime.now()
        })

while True:
	msg = input('Enter a message: ')
	msg_funct(msg, s)

s.close()
