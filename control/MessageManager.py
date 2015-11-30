from control.socket.client import Client
from control.socket.server import Server
from control.json_parser.parser import Parser

class MessageManager(object):
    
    parser = Parser()
    server = Server(0)
    client = Client(1)
    myIp = None
    manager = None
    
    def __init__(self):
        self.server.setManager(self)
        
    def setMyIp(self, ip):
        self.myIp = ip
        self.parser.setMyIp(self.myIp)
        
    def setManager(self, manager):
        self.manager = manager
        self.parser.setManager(manager)