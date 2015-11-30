import socket
from threading import Thread
from threading import Timer
from time import sleep
from control.json_parser.parser import Parser


class Server(Thread):

	UDP_PORT = 9000
# 	UDP_IP = '127.0.0.1'
# 	UDP_IP = '<broadcast>'
	UDP_IP = ''
	_keepRunning = True
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	manager = None
	

	def __init__(self, threadID):
		Thread.__init__(self)
		self.num = threadID
		self.sock.settimeout(2)

	def stop(self):
		self._keepRunning = False
	def setManager(self, m):
		self.manager = m

	def run(self):
# 		self.sock.bind(('<broadcast>', self.UDP_PORT))
		self.sock.bind((self.UDP_IP, self.UDP_PORT))
		while self._keepRunning:
			try:
				msg = self.sock.recvfrom(1024)
			except socket.timeout, e:
				err = e.args[0]
				if err == 'timed out':
					sleep(1)
					continue
				else:
					print e
			except socket.error, e:
				print e
			else:
				if len(msg) == 0:
					print 'received an empty message', " from ", msg[1][0]
				else:
# 					print "Received ", msg[0], " from ", msg[1][0]
					self.manager.parser.decode(msg[0],msg[1][0]);
		print "Stopping Server"