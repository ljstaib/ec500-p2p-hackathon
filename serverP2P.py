#!/usr/bin/env python3
#Adapted from https://stackoverflow.com/questions/21233340/sending-string-via-socket-python for educational purposes

#Luke Staib, ljstaib@bu.edu, 2021

import socket
from threading import *
import pymongo
import datetime

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb')
db = client['test']

#discovery
discoveryclient = pymongo.MongoClient('mongodb+srv://Brian:cyp1b1@cluster0.v056q.mongodb.net/FileDB?retryWrites=true&w=majority')
discoverydb = discoveryclient['FileDB']
collection = discoverydb['Users']

collection.find


# Luke running server, remote client
HOST = '155.41.17.114'
PORT = 5000
print(db)
#Client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reset tcp server
s.bind((HOST,PORT))

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
			print('User 1 sent: ', data)
			msg = input('Enter a message: ')
			self.s.send(msg.encode()) 
			db.messages.insert_one(
    			{
					"Sender" : "Alice",
					"Receiver" : "Bob",
					"Text" : data,
					"Timestamp" : datetime.datetime.now()
				}
)

s.listen(5)

while True:
	s, addr = s.accept()
	client(s, addr)
