from Tkinter import Tk, Menu, Listbox, Entry, Text, Checkbutton, IntVar, Button, END
import tkMessageBox
from model.User import User
from model.Message import Message
import pyaudio
import wave

class UserInterface:
    
    root = Tk()
    menubar = Menu(root)
    listbox = Listbox(root)
    input = Entry(root,text = 'input your text here',width = 105)
    text = Text(root, height=10, width=120)
    checkWhisper = IntVar()
    manager = None
    checkButton = Checkbutton(root, text="Whisper", variable=checkWhisper)
    usersListBox = {}
    
    def __init__(self):
        
        self.root.title("Chat")
        self.root.bind("<Escape>", self.terminate)
        self.root.minsize(888, 250) 
        
        self.menubar.add_command(label="Exit", command=self.terminate)
        self.root.config(menu=self.menubar)
        
        self.checkButton.grid(row=0)
        self.checkButton.configure(state="disabled")
        
        
        self.listbox.insert(END, "talk to everyone")    
        self.listbox.grid(row=1, pady=10,padx=5)
        self.listbox.selection_set(first=0)
        self.listbox.bind('<<ListboxSelect>>', self.onListBoxChanged)
        
        self.input.focus()
        self.input.bind('<Return>', self.sendPressed)
        self.input.grid(row=2, column=1)
        
        
        self.text.configure(state="disabled")
        self.text.grid(row=1, column=1,pady=10,padx=10)
        
        button = Button(self.root, text="Enviar", command= lambda: self.sendPressed())
        button.grid(row=2, column=0, pady=10,padx=10)
    
    def onListBoxChanged(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
#         value = w.get(index)
        
        if (index == 0):
            self.checkButton.configure(state="disabled")
            self.checkButton.deselect()
        else:
            self.checkButton.configure(state="normal")
#         print 'You selected item %d: "%s"' % (index, value)
        
    
    def sendPressed(self, inp = None):
        
        try:
            text = self.input.get()
            index = int(self.listbox.curselection()[0])
            if(self.checkWhisper.get()):
                message = Message(text, self.manager.myIp, 'whisper')
                users = self.manager.contactManager.users
                user = users[self.usersListBox[index]].nickname()
                self.manager.messageManager.client.sendTo(self.usersListBox[self.listbox.curselection()[0]], self.manager.messageManager.parser.codeWhisper(message))
                self.sendToUI("You -> " + user + ": " + message.content())
                
            else:
                message = Message(self.input.get(), self.manager.contactManager.mySelf, "say")
                if(int(self.listbox.curselection()[0]) != 0):
                    message._to = self.usersListBox[self.listbox.curselection()[0]]
                self.printMessage(message)
                self.manager.messageManager.client.sendBroadcast(self.manager.messageManager.parser.codeSay(message))    
            self.input.delete(0, 'end')
                    
        except Exception as e:
            print "Error on sendPressed: ", e

    def printMessage(self, msg):
        try:
            text = ""
            
            msgIP = str(msg.user().ip())
            myIp = str(self.manager.contactManager.mySelf.ip())
            
            print msgIP
            print myIp
            
            if msg._to is not None:
                if (msgIP == myIp):
                    text = "You => " + self.manager.contactManager.users[msg._to].nickname() +": " + msg.content()
                else:
                    text = msg.user().nickname() + ' => You: ' + msg.content()
            else:
                if (msgIP == myIp):
                    text = 'You: ' + msg.content()
                else:
                    text = msg.user().nickname() + ': ' + msg.content()
                
            self.sendToUI(text)
        except KeyError as e:
            print "Error on printmessage: could not parse", e
        except Exception as e:
            print "Error on printmessage: ", e
        
    def sendToUI(self, msg):
        try:
            self.text.configure(state="normal")
            self.text.insert(END, msg + '\n')
            self.text.see(END)
            self.text.configure(state="disabled")
        except Exception as e:
            print "sendToUI: ", e
        
    
    def setManager(self, m):
        self.manager = m
    
    def setParser(self, newparser):
        self.parser = newparser
    
    def messageReceived(self, message):
        self.printMessage(message)
        self.playSound("sounds/msn.wav")
    
    def whisperReceived(self, message):
        self.sendToUI(message)
        self.playSound("sounds/icq.wav")
        
    def playSound(self, filepath):
        sound = wave.open(filepath)
        p = pyaudio.PyAudio()
        chunk = 1024
        stream = p.open(format =
                        p.get_format_from_width(sound.getsampwidth()),
                        channels =  sound.getnchannels(),
                        rate = sound.getframerate(),
                        output = True)
        data = sound.readframes(chunk)
        while data != '':
            stream.write(data)
            data = sound.readframes(chunk)
        p.terminate()
                
    def terminate(self, arg = None):
        if tkMessageBox.askyesno("Exit", "Are you sure?"):
            self.root.quit()
            
    def addContact(self, user):
        try:
            self.listbox.insert(END, user.nickname() + " (" + user.ip() + ")")
            self.usersListBox[int(self.listbox.size() - 1)] = user.ip()
            self.playSound("sounds/online.wav")
        except Exception as e:
            print "Error on addContact: ", e
            
    def insertContact(self, user):
        try:
            self.listbox.insert(END, user.nickname() + " (" + user.ip() + ")")
            self.usersListBox[int(self.listbox.size() - 1)] = user.ip()
        except Exception as e:
            print "Error on addContact: ", e
    
    def reloadContacts(self):
        self.usersListBox.clear()
        self.listbox.delete(0, END)
        self.listbox.insert(END, "talk to everyone")
        for the_key, the_value in self.manager.contactManager.users.iteritems():
            self.insertContact(the_value)
        
    def run(self):
        self.reloadContacts()
        self.root.mainloop()