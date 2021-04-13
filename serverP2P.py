#!/usr/bin/env python3
#Adapted from https://stackoverflow.com/questions/21233340/sending-string-via-socket-python for educational purposes

#Luke Staib, ljstaib@bu.edu, 2021

import socket
from threading import *
import pymongo
import datetime
import urllib.request, json

#local message storage inits
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')
db = client['test']

#discovery inits
discoveryclient = pymongo.MongoClient('mongodb+srv://Brian:cyp1b1@cluster0.v056q.mongodb.net/FileDB?retryWrites=true&w=majority')
discoverydb = discoveryclient['FileDB']
collection = discoverydb['Users']

#Auto update IP
ipv4 = json.loads(urllib.request.urlopen("http://ip.jsontest.com/").read())
print(ipv4["ip"])

Name = input("Who are you?")
collection.update_one({"Name" : Name}, {"$set" : {"IP" : ipv4["ip"]}})

#Discovery
#print discoverable users
friends = collection.find({"Discoverable" : True})

for person in friends:
    print(person["Name"])
    
receiver = input("Whom would you like to talk to? Please choose from the list above:")
receiverDoc = collection.find_one({"Name" : receiver})

#Server starts server on local machine 
HOST = ipv4["ip"]


#UPDATE SENDER AND RECEIVER TO BE DYNAMIC + LIST ALL MESSAGES
pastmessages = db.messages.find({"$or" : [{"$and" : [{"Sender" : Name}, {"Receiver" : receiver}]}, {"$and" : [{"Sender" : receiver },{"Receiver" : Name}]}]})
for messages in pastmessages:
    print("[", messages["Timestamp"],"] ", messages["Sender"], ": ",messages["Text"] )

# Luke running server, remote client
#HOST = '127.0.0.1'
PORT = 5000

#Client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reset tcp server
s.bind((HOST,PORT))
print("SOCKET BOUND")
class client(Thread):
	def __init__(self, socket, address):
		Thread.__init__(self)
		self.s = socket
		self.addr = address
		self.start()

	def run(self):
		print("Running")
		while True:
			data = self.s.recv(1024).decode()
			print(receiver,' sent: ', data)
			msg = input('Enter a message: ')
			self.s.send(msg.encode())
			#save received message
			db.messages.insert_one(
				{
					"Sender" : receiver,
					"Receiver" : Name,
					"Text" : data,
					"Timestamp" : datetime.datetime.now()
				})
			#save sent message
			db.messages.insert_one(
				{
					"Sender" : Name,
					"Receiver" : receiver,
					"Text" : msg,
					"Timestamp" : datetime.datetime.now()
				})

s.listen(5)

while True:
	s, addr = s.accept()
	client(s, addr)
