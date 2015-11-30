import time
from datetime import datetime
class User(object):
    
    _ip = None
    _nickname = None
    _lastKeepAlive = None

    def __init__(self, ip, nickname):
        self._ip = ip
        self._nickname = nickname
        self._lastKeepAlive = datetime.now()
    
    def ip(self):
        return self._ip
    
    def nickname(self):
        return self._nickname
    
    def lastKeepAlive(self):
        return self._lastKeepAlive
    
    def keepAlive(self):
        self._lastKeepAlive = datetime.now()
    
        