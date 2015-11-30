from model.User import User
from time import sleep
import datetime
from threading import Thread

class ContactManager(Thread):
    
    users = {};
    mySelf = User("127.0.0.1", "Michael")
    manager = None
    keepRunning = True
    
    def __init__(self, id):
        Thread.__init__(self)
        self.num = id
        self.users.clear()
        
    def setManager(self, manager):
        self.manager = manager
        
    def keepUserAlive(self, ip):
        if ip in self.users:
            self.users[ip].keepAlive()
        else:
            print "keepUserAlive: user not found"
    
    def addContact(self, user):
        print "adding user: ", user.nickname(), " on ", user.ip()
        self.users[user.ip()] = user
    
    def removeContact(self, ip):
        del self.users[ip]
        
    def getMySelf(self):
        return self.mySelf
    
    def run(self):
        while(self.keepRunning):
            if(len(self.users) > 0):
                itensToremove = []
                data = self.manager.messageManager.parser.codeKeepAlive()
                for the_key, the_value in self.users.iteritems():
                    now = datetime.datetime.now()
                    elapsed = now - the_value.lastKeepAlive()
                    if elapsed > datetime.timedelta(seconds=60):
                        itensToremove.append(the_key)
                if len(itensToremove) > 0:
                    for item in itensToremove:
                        print self.users[item].nickname() + " was removed by inactivity"
                        self.removeContact(item)
                        self.manager.myUI.reloadContacts()
                self.sendMulticast(data)
                sleep(10)
            else:
                print "Searching"
                data = self.manager.messageManager.parser.codeSearch()
                self.manager.messageManager.client.sendBroadcast(str(data))
                sleep(2)
                
    def stop(self):
        self.keepRunning = False
            
    def sendMulticast(self, message): 
        for the_key, the_value in self.users.iteritems():
            self.manager.messageManager.client.sendTo(the_key, str(message))
            the_value