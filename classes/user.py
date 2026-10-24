from typing import List

from twisted.words.protocols.irc import IRC

from classes.channel import Channel


class User:
    protocol : IRC
    nick: str
    hostname: str
    registered: bool = False
    chans : List[Channel] = []

    def __init__(self, nick,protocol):
        self.protocol: IRC = protocol
        self.nick: str = nick


    def register(self,hostname):
        if self.registered:
            return False

        self.hostname = hostname
        self.registered = True

        return True

    def name(self):
        return f"{self.nick}!{self.nick}@{self.hostname}"
