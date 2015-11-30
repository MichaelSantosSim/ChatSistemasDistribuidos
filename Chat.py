from view.UI import UserInterface
from control.ContactManager import ContactManager
from control.MessageManager import MessageManager

class Chat(object):
    
    myUI = UserInterface()
    myIp = None
    contactManager = ContactManager(5)
    messageManager = MessageManager()
    
    def __init__(self,ip):
        self.myIp = ip 
        self.myUI.setManager(self)
        self.messageManager.setMyIp(self.myIp)
        self.messageManager.setManager(self)
        self.contactManager.setManager(self)
        self.contactManager.mySelf._ip = ip
        
    def run(self):
        self.messageManager.server.start()
        self.contactManager.start()
        self.myUI.run()
        parser = self.messageManager.parser
        client = self.messageManager.client
        client.sendBroadcast(parser.codeLeave())
        self.contactManager.stop()
        self.messageManager.server.stop()