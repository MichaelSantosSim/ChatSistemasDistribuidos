'''
Created on Nov 15, 2015

@author: michael
'''

class Message(object):
    
    
    _content = None     # conteudo da mensagem
    _user = None        # qual o usuario
    _action = None      # acao que pode ser whisper ou say
    _to     = None      # para quem vai
    
    def __init__(self, text, user, action):
        self._content = text
        self._user = user
        self._action = action
    
    def user(self):
        return self._user
    
    def content(self):
        return self._content
    
    def action(self):
        return self._action