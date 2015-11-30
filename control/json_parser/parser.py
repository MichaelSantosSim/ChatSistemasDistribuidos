import json,ast
from model.User import User
from model.Message import Message

class Parser(object):
	
	manager = None
	myIp = None
	
	def setMyIp(self, ip):
		self.myIp = ip
	
	def searchRequest(self, parsed_json, sourceAddress):
		try:
			if not sourceAddress in self.manager.contactManager.users:
				user = User(sourceAddress, parsed_json['nickname'])
				self.manager.contactManager.addContact(user)
				self.manager.messageManager.client.sendTo(sourceAddress, self.codeKeepAlive())
				self.manager.myUI.addContact(user) 
				print parsed_json['nickname'], " entered the room"
		except KeyError as e:
			print "Error on searchRequest: could not parse", e
		except Exception as e:
			print "Error on searchRequest: ", e
	
	def keepAliveRequest(self, parsed_json, sourceAddress):
		try:
			if not sourceAddress in self.manager.contactManager.users:
				user = User(sourceAddress, parsed_json['nickname'])
				self.manager.contactManager.addContact(user)
				self.manager.messageManager.client.sendTo(sourceAddress, self.codeKeepAlive())
				self.manager.myUI.addContact(user)
			for item in parsed_json['users']:
				if not item['address'] in self.manager.contactManager.users and item['address'] != self.myIp:
					user = User(item['address'], item['nickname'])
					self.manager.contactManager.addContact(user)
					self.manager.messageManager.client.sendTo(sourceAddress, self.codeKeepAlive())
					self.manager.myUI.addContact(user)
			else:
				print "keeping user alive: " + sourceAddress
				self.manager.contactManager.keepUserAlive(sourceAddress)
		except KeyError as e:
			print "Error on Parser.keepAliveRequest() could not parse ", e
		except Exception as e:
			print "Error on Parser.keepAliveRequest(): ", e

	def sayRequest(self, parsed_json, sourceAddress):
		try:
			if sourceAddress in self.manager.contactManager.users:
				user = self.manager.contactManager.users[sourceAddress]
				message = Message(parsed_json['content'], user, 'say')
				if 'target' in parsed_json:
					if parsed_json['target'] in self.manager.contactManager.users:
						message._to = self.manager.contactManager.users[parsed_json['target']].nickname()
					elif parsed_json['target'] == self.myIp:
						message._to = str(self.myIp)
					else:
						message._to = parsed_json['target']
				self.manager.myUI.messageReceived(message)
			else:
				print "Mensagem de um desconhecido: ", parsed_json['content']
		except KeyError as e:
			print "Error on Parser.sayRequest() could not parse ", e
		except Exception as e:
			print "Error on Parser.sayRequest(): ", e

	def whisperRequest(self, parsed_json, sourceAddress):
		try:
			text = ""
			if sourceAddress in self.manager.contactManager.users:
				text = self.manager.contactManager.users[sourceAddress].nickname() + " -> You: " + parsed_json['content']
			else:
				text = sourceAddress + " -> You: " + parsed_json['content']
			self.manager.myUI.whisperReceived(text)
			
		except KeyError as e:
			print "Error on Parser.whisperRequest() could not parse", e
		except Exception as e:
			print "Error on Parser.whisperRequest(): ", e

	def leaveRequest(self, parsed_json, sourceAddress):
		try:
			if sourceAddress in self.manager.contactManager.users:
				users = self.manager.contactManager.users
				print users[sourceAddress].nickname(), " left the room"
				del users[sourceAddress]
				self.manager.myUI.reloadContacts()
			else:
				print "Could not remove user: ", sourceAddress
		except KeyError as e:
			print "Error on Parser.leaveRequest() could not parse ", e
		except Exception as e:
			print "Error on Parser.leaveRequest()", e

	def reportRequest(self, parsed_json, sourceAddress):
		try:
			print "Report from: ", sourceAddress, "  ", parsed_json['message']
		except KeyError as e:
			print "Error on Parser.reportRequest(), could not parse ", e
		except Exception as e:
			print "Error on Parser.reportRequest(): ", e
	
	def setManager(self, m):
		self.manager = m

	def decode(self, text, sourceAddress):
		try:
			if not(self.myMessage(sourceAddress)):
				parsed_json = json.loads(text)
				self.dict[parsed_json['action']](self, parsed_json, sourceAddress)
		except KeyError as e:	
			print "Error on decode Could not decode action:", e
	
	def codeSay(self, message):
		try:
			data = {}
			data ['action'] = 'say'
			data['content'] = message.content()
			if message._to is not None:
				data['target'] = message._to
			data = json.dumps(data)
			return data
		except:
			print "Convert Error"
		
	def codeSearch(self):
		try:
			data = {}
			data['action'] = 'search'
			data['nickname'] = self.manager.contactManager.getMySelf().nickname()
			data = json.dumps(data)
			return data
		except Exception as e:
			print "Code Search Error: ", e
			
	def codeKeepAlive(self):
		try:
			data = {}
			data['action'] = 'keepAlive'
			data['nickname'] = data['nickname'] = self.manager.contactManager.getMySelf().nickname()
			data['users'] = []
			for the_key, the_value in self.manager.contactManager.users.iteritems():
				data["users"].append({"nickname" : the_value.nickname().encode("utf-8"), "address" : the_key})
			data = json.dumps(data)
			return data
		except Exception as e:
			print "codeKeepAlive Error: ", e
		
	def codeWhisper(self, message):
		try:
			data = {}
			data ['action'] = 'whisper'
			data['content'] = message.content()
			data = json.dumps(data)
			return data
		except:
			print "Convert Error"
	
	def codeLeave(self):
		try:
			data = {}
			data ['action'] = 'leave'
			data = json.dumps(data)
			return data
		except:
			print "Convert Error"
	
	def myMessage(self, ip):
		if(ip == self.myIp):
			return True
		else:
			return False

	dict = {'search': searchRequest,
			'keepAlive': keepAliveRequest,
			'say': sayRequest,
			'whisper':whisperRequest,
			'leave': leaveRequest,
			'report': reportRequest};
			