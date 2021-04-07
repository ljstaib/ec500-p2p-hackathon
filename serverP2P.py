#!/usr/bin/env python3
#Adapted from https://stackoverflow.com/questions/21233340/sending-string-via-socket-python for educational purposes

#Luke Staib, ljstaib@bu.edu, 2021

import socket
from threading import *

HOST = '127.0.0.1'
PORT = 12348

#Client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))

class client(Thread):
	def __init__(self, socket, address):
		Thread.__init__(self)
		self.s = socket
		self.addr = address
		self.start()

	def run(self):
		while True:
			print('User 1 sent: ', self.s.recv(1024).decode())
			msg = input('Enter a message: ')
			self.s.send(msg.encode()) 

s.listen(5)

while True:
	s, addr = s.accept()
	client(s, addr)