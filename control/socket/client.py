	#!/usr/bin/python

from threading import Thread
import socket
from socket import error as socket_error

class Client(Thread):

	UDP_PORT = 9000

	def __init__(self, threadID):
		Thread.__init__(self)
		self.num = threadID

	def sendBroadcast(self, message):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind(('',0))
			sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# 			print "Sending BroadCast"+
# 			print message
			sock.sendto(message, ('<broadcast>', self.UDP_PORT))
		except socket_error as serr:
			print "Client.run() - ", serr
		
	def sendTo(self, ip, message):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 		print "Sending message to: ", ip
# 		print message
		sock.sendto(message, (ip, self.UDP_PORT))